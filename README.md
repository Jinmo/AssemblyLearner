# AssemblyLearner
어셈블리어를 배워서 써먹자. (x86 지원)

## Installation

```
$ sudo apt-get install python3-dev # 필요에 따라 redis-server 설치
$ pip install -r requirements.txt
```

Docker
```
docker run -d -p 3333:<외부에서 연결하기를 원하는 포트> bunseokbot/jinmo-asm-learner:latest
```

## Introduction
이 소스코드는 어셈블리어를 배우는 사이트에 대한 소스코드입니다.
문제도 추가할 수 있어요!

## How-to
사용 방법을 알려드릴게요.

### 문제 관련
문제를 추가하시려면

0. 관리자 계정 추가 후
0. 로그인 후 Admin 메뉴를 통해 관리자 화면으로 들어가서
0. Problems 메뉴의 문제 추가를 누른 후 각종 정보를 추가한 뒤
0. Add Problem을 누르면 문제가 바로 추가됩니다!

### 문제 작성 시 입력하는 정보
- 문제 이름 (Name)
문제로 표시될 이름이에요.
- 분류 (Category)
분류는 입력하는대로 추가되요.
- 문제 설명 (Instruction)
문제에 대한 내용을 채워넣으시면 됩니다.
- 사용자가 작성한 코드 뒤에 추가될 코드 (Suffix)
프로그램 시작점인 _start 등을 넣으면 됩니다.
- 예제 (Example)
코드 창에 미리 표시될 코드입니다. 이 코드 기반으로 사용자들이 풀 수 있어요.
- 힌트 (Hint)
문제에 대한 힌트를 적으면 됩니다. 표시는 추후 추가할거에요.
- 답 정규식 (Answer)
해답을 적으면 됩니다.

### suffix.txt 관련
보통 문제 만들 때 검증 코드를 넣을 때가 있잖아요?
그럴 때는 예제 코드에다가 _start가 아닌 다른 함수를 정의하게 한 다음 _start에서 그 함수를 호출해서 결과를 비교하는 방식으로 짤 수 있어요.

## Dependencies
- Python 3.4 (tested on 3.4.3)
- Flask for Python (http://flask.pocoo.org)
- gcc compiler (tested on 4.8.4)
- eventlet (동작하는지도 잘 모르겠네요..)
- RQ (Redis Queue) for Python
