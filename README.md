# AssemblyLearner
어셈블리어를 배워서 써먹자. (x86 지원)

## Installation

```
$ sudo apt-get install python-dev
$ pip install -r requirements.txt
```

## Introduction
이 소스코드는 어셈블리어를 배우는 사이트에 대한 소스코드입니다.
문제도 추가할 수 있어요!

## How-to
사용 방법을 알려드릴게요. 참고로 관리자용 인터페이스같은거 안 만들었어요.

### 문제 관련
문제를 추가하시려면

0. problem/카테고리_문제이름/ 폴더를 만드신 후
0. 폴더 안에 info.txt (문제 이름 / 문제 순서 변경에 쓰일 사전순으로 정렬될 구분자, 숫자로 하면 되요)를 만들고
0. 폴더 안에 example.txt (코드 쪽에 기본적으로 보일 예제 비스무리한 코드)를 만들고
0. 폴더 안에 answer.txt (문제에서 답을 출력시킬 때)를 만들고
0. 폴더 안에 instruction.txt (문제 지문)를 만들고
0. 폴더 안에 suffix.txt (문제 코드 뒤에 붙을 어셈블리어 코드)를 만들고

내용을 채워넣으시면 됩니다!

그 다음 /_load_problems를 넣으시면 문제가 로딩되요!
필요에 따라 잘 수정해보세요.

### suffix.txt 관련
보통 문제 만들 때 검증 코드를 넣을 때가 있잖아요?
그럴 때는 예제 코드에다가 _start가 아닌 다른 함수를 정의하게 한 다음 _start에서 그 함수를 호출해서 결과를 비교하는 방식으로 짤 수 있어요.

## Dependencies
- Python 2.7 (tested)
- Flask for Python (http://flask.pocoo.org)
- gcc compiler
- eventlet (동작하는지도 잘 모르겠네요..)
