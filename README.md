# AutoBlog

블로그 최적화 링크 열기 작업을 자동화하는 Python 스크립트입니다.

현재 프로젝트의 메인 실행 파일은 `blogAuto.py`입니다.

## 필요한 패키지

현재 코드 기준으로 아래 패키지가 필요합니다.

- `selenium`
- `webdriver-manager`

`requirements.txt`에 정리되어 있으므로 아래 명령으로 한 번에 설치할 수 있습니다.

## 설치 방법

### 1. Python 준비

- 권장 버전: Python 3.11
- Python 3.9 이상에서도 동작 가능성은 있지만, 가능한 한 3.11 환경을 권장합니다.
- 가상환경을 Python 3.11로 만들려면, `venv` 생성 명령도 반드시 Python 3.11 인터프리터로 실행해야 합니다.

### 방법 A. 가상환경 사용

프로젝트별로 패키지를 분리해서 관리하고 싶다면 이 방법을 권장합니다.

macOS / Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

이미 `.venv`를 다른 Python 버전으로 만든 상태라면 삭제 후 다시 생성합니다.

macOS / Linux:

```bash
rm -rf .venv
```

Windows:

```bash
rmdir /s /q .venv
```

가상환경을 활성화한 뒤 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

### 방법 B. 전역 환경에 바로 설치

가상환경을 만들지 않고 현재 Python 환경에 바로 설치하는 방법입니다.

macOS / Linux:

```bash
pip3 install -r requirements.txt
```

Windows:

```bash
pip install -r requirements.txt
```

## 실행 방법

설치 방법에 따라 실행 순서가 달라집니다.

### 방법 A로 설치한 경우: 가상환경을 먼저 활성화한 뒤 실행

가상환경 방식으로 설치했다면, `python` 명령이 `.venv` 안의 Python을 가리키도록 먼저 활성화해야 합니다.

즉, 아래 순서로 실행합니다.

1. 프로젝트 폴더로 이동
2. 가상환경 활성화
3. `python blogAuto.py` 실행

macOS / Linux:

```bash
cd /Users/hyuntae/IdeaProjects/AutoBlog
source .venv/bin/activate
python blogAuto.py
```

Windows:

```bash
cd /d C:\path\to\AutoBlog
.venv\Scripts\activate
python blogAuto.py
```

활성화가 정상적으로 되면 터미널 앞에 보통 `(.venv)`가 표시됩니다.

예시:

```bash
(.venv) hyuntae@MacBookPro AutoBlog %
```

이 상태에서 실행하는 `python`은 가상환경 안의 Python입니다.

### 방법 B로 설치한 경우: 바로 실행

전역 환경에 설치했다면 가상환경 활성화는 필요 없습니다.

macOS / Linux:

```bash
python3 blogAuto.py
```

Windows:

```bash
python blogAuto.py
```

### 다음부터 다시 실행할 때

가상환경 방식이라면 프로그램을 다시 실행할 때마다 `source .venv/bin/activate`를 먼저 해야 합니다.

즉, macOS에서는 보통 아래 두 줄만 기억하면 됩니다.

```bash
source .venv/bin/activate
python blogAuto.py
```

터미널을 새로 열 때마다 가상환경 활성화는 다시 해줘야 합니다.

### VSCode에서 실행하기

VSCode를 사용한다면 `blogAuto.py` 파일을 연 뒤 우측 상단의 `Run Python File` 버튼으로 실행할 수 있습니다.

다만 실행 전에 VSCode가 사용할 Python 인터프리터가 올바르게 선택되어 있어야 합니다.

- 가상환경을 사용했다면 Python 3.11 기반의 `.venv` 인터프리터를 선택합니다.
- 전역 설치를 사용했다면 패키지가 설치된 기본 Python 인터프리터를 선택합니다.

일반적인 순서는 아래와 같습니다.

1. VSCode에서 프로젝트 폴더를 엽니다.
2. `blogAuto.py`를 엽니다.
3. `Python: Select Interpreter`로 사용할 Python 환경을 선택합니다.
4. 우측 상단의 `Run Python File` 버튼을 누릅니다.

## 입력 파일

- `KakaoTalk*.txt` 형식의 파일을 프로젝트 루트 폴더에 두고 실행해야 합니다.
- 스크립트는 가장 최근 수정된 `KakaoTalk*.txt` 파일을 읽습니다.

예시:

```text
KakaoTalk_Chat_2026-04-04-01-00-03.txt
```

## 동작 방식

1. Chrome 브라우저를 엽니다.
2. 네이버 로그인 페이지로 이동합니다.
3. 사용자가 직접 로그인합니다.
4. 터미널에서 `p`를 입력하고 Enter를 누르면 링크 추출을 진행합니다.
5. 일반 링크를 먼저 열고, `/clip/` 링크를 나중에 엽니다.
6. 프로그램이 계속 대기하다가 `q`를 입력하고 Enter를 누르면 `KakaoTalk*.txt` 파일을 삭제하고 종료합니다.

## macOS에서 주의할 점

- Google Chrome이 설치되어 있어야 합니다.
- 처음 실행 시 `webdriver-manager`가 ChromeDriver를 다운로드할 수 있도록 인터넷 연결이 필요할 수 있습니다.
- 현재 버전은 터미널 입력 방식으로 동작하므로, macOS와 Windows에서 별도의 키보드 접근성 권한 없이 사용할 수 있습니다.

## 빠른 시작

### 가상환경 방식

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python blogAuto.py
```

### 전역 설치 방식

```bash
pip3 install -r requirements.txt
python3 blogAuto.py
```
