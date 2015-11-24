#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/param.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <syscall.h>
#include <errno.h>

typedef struct {
  int sysno;
  char *name;
} syscallDesc;

syscallDesc syscallDescs[] = {
  {__NR_exit, "exit"},
  {__NR_read, "read"},
  {__NR_write, "write"},
  {__NR_open, "open"},
  {__NR_exit_group, "exit_group"},
  {__NR_execve, "execve"},
  {__NR_futex, "futex"},
  {__NR_geteuid, "geteuid"},
  {__NR_getuid, "getuid"},
  {__NR_getegid, "getegid"},
  {__NR_getgid, "getgid"},
  {__NR_close, "close"}
};

int pid = -1;

void line() {
	puts("-----------------------------\n");
}

void dump_regs(struct user_regs_struct *_user) {
  printf("register dump at %08x\n", _user->eip);
	printf(" EAX=%08x EBX=%08x\n", _user->eax, _user->ebx);
	printf(" ECX=%08x EDX=%08x\n", _user->ecx, _user->edx);
	printf(" EDI=%08x ESI=%08x\n", _user->edi, _user->esi);
	printf(" EBP=%08x ESP=%08x\n", _user->ebp, _user->esp);
  puts("");
}

void get_string(long long addr, char *buf, int len) {
	long tmp_buf;
	int i, j = 0;
#define word_len sizeof(long)
	for(i = 0; i < len - 1; i += word_len) {
		tmp_buf = ptrace(PTRACE_PEEKDATA, pid, addr + i, 0);
		if(tmp_buf == -1) {
			break;
		}
		for(j = 0; j < word_len; j++) {
			if(((char *)&tmp_buf)[j] == '\0')
				break;
		}
		if(i + j > len) j = len - i - 1;
		memcpy(buf + i, &tmp_buf, j);
		if(j != word_len) break;
	}
	buf[i >= len - 1 ? len - 1: i + j] = '\0';
}

int main(int argc, char **argv) {
  bool soft_exit = false,
       first_syscall = true;

  alarm(1); // execution time limit

	if(argc < 4) {
		return -1;
	}

	struct user_regs_struct _user;

	freopen(argv[2], "rb", stdin);
	freopen(argv[3], "wb", stdout);

  setvbuf(stdout, 0, _IONBF, 0);

	pid = fork();
	if(pid == 0) {

		// ptrace init
		if(ptrace(PTRACE_TRACEME) == -1) exit(1);

		// execute target
		execl(argv[1], argv[1], NULL);

		return -1; // if reaches here, it must be error in execve.
	} else {

    usleep(50000);
    ptrace(PTRACE_SETOPTIONS, pid, 0, PTRACE_O_TRACESYSGOOD | PTRACE_O_TRACEEXIT | PTRACE_O_TRACEEXEC);

		while(!soft_exit) {
			int status;
			int w = waitpid(pid, &status, WCONTINUED);
			int sysno;
			bool pass = false;
			char cmd_buf[1024];
      char path_buf[MAXPATHLEN];

			if(w == -1) {
				printf("Process exited, status: %d\n", status);
				return 0;
			}

			if(WIFEXITED(status)) {
        if(soft_exit) {
          line();
          printf("Program Ended (unknown error)\n");
        }
				break;
      } else if(WIFSTOPPED(status)) {

        ptrace(PTRACE_GETREGS, pid, &_user, &_user);

//      printf("Interrupt %x invoked\n", WSTOPSIG(status));
        fflush(stdout);

        switch(WSTOPSIG(status)) {
        case 0x80 | SIGTRAP:
        case SIGTRAP:
          {

          sysno = _user.orig_eax;
          if(first_syscall) { // at program start
            first_syscall = false;
            ptrace(PTRACE_SYSCALL, pid, 0, 0);
            continue; // for outer loop
          } else {
            if(sysno == -1) {
              dump_regs(&_user);
              ptrace(PTRACE_CONT, pid, 0, 0);
              continue;
            }

            char *syscallName = NULL;
            char syscallNameBuf[256];
            int index;
            for(index = 0; index < sizeof(syscallDescs) / sizeof(syscallDesc); index++) {
              if(sysno == syscallDescs[index].sysno) {
                syscallName = syscallDescs[index].name;
                break;
              }
            }

            if(syscallName == NULL) {
              snprintf(syscallNameBuf, sizeof(syscallNameBuf) - 1, "number: %d", sysno);
              syscallName = syscallNameBuf;
            }
            printf("Syscall invoked ! (%s)\n", syscallName);
            _user.eax = _user.orig_eax;
            dump_regs(&_user);
            switch(sysno) {
              case __NR_fork:
              case __NR_clone:
                pass = false;
                break;
              case __NR_write:
              case __NR_read:
                pass = true;
                break;
              case __NR_open:
                pass = true;
                break;
              case __NR_exit:
              case __NR_exit_group:
                line();
                printf("Program Exited (exit code: %d)\n", (unsigned int)_user.ebx);
                pass = true;
                soft_exit = true;
                break;
              case __NR_execve:
                if(_user.ebx == 0) {
                  pass = true;
                  break;
                }
#if DEBUG
                fprintf(stderr, "execve path: %p\n", _user.ebx);
#endif
                get_string(_user.ebx, (char *)&cmd_buf, 1024);
                realpath(cmd_buf, path_buf);
                printf("execve: %s realpath: %s\n", cmd_buf, path_buf);
                if(!strcmp(path_buf, "/bin/sh") || !strcmp(path_buf, "/bin/dash")) {
                  puts("[user@ubuntu:~] $ id\nuid=1000(user) gid=1000(user) groups=1000(user)");
                  kill(pid, 9);
                  line();
                  return 0;
                } else if(!strcmp(path_buf, "/bin/ls")) {
                  puts("flag\tin\tout");
                  kill(pid, 9);
                  line();
                  return 0;
                }
                pass = false;
                execve(path_buf, 0, 0);
                break;
              case __NR_getresgid:
              case __NR_getresuid:
              case __NR_getuid:
              case __NR_getgid:
              case __NR_setreuid:
              case __NR_setregid:
              case __NR_futex:
                pass = true;
                break;
              default:
                pass = false;
            }
          }

          if(pass == true)
            ptrace(PTRACE_SYSCALL, pid, 0, 0);
          else {
            line();
            printf("Program Ended (blacklisted, syscall: %d)\n", sysno);
            kill(pid, 9);
            return -1;
            break;
          }
        }
        break;
        case SIGTRAP | 0x1000:
          if(_user.orig_eax == -1) {
            // TRAP for DUMP REGS
            dump_regs(&_user);
            ptrace(PTRACE_CONT, pid ,0, 0);
          } else {
            ptrace(PTRACE_SYSCALL, pid, 0, 0);
          }
          break;

        case SIGSEGV:
          puts("Segmentation fault");
          dump_regs(&_user);
          kill(pid, 9);
          soft_exit = 1;
          break;
        default:
          printf("Unsupported signal: %d\n", WSTOPSIG(status));
          kill(pid, 9);
          break;
        }
      }
    }
	}
}
