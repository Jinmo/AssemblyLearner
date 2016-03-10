CC=gcc
OBJS=tracer.o
TARGET=tracer
CFLAGS:=-m32

.SUFFIXES: .c, .o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

clean:
	rm -f $(OBJS) $(TARGET)
