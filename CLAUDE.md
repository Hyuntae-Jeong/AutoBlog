# CLAUDE.md

## Project Overview

네이버 블로그 최적화 작업 자동화 스크립트. 카카오톡 채팅방에서 내보낸 텍스트 파일(`KakaoTalk*.txt`)에서 네이버 블로그 링크를 추출하고, Chrome 브라우저에서 자동으로 열어주는 Python 스크립트.

## Tech Stack

- Python 3.11
- Selenium (브라우저 자동화)
- webdriver-manager (ChromeDriver 자동 관리)

## Project Structure

```
blogAuto.py        # 메인 스크립트 (유일한 소스 파일)
requirements.txt   # 의존성 (selenium, webdriver-manager)
todo.txt           # 향후 작업 목록
KakaoTalk*.txt     # 입력 파일 (gitignore 대상)
```

## How It Works

1. Chrome 실행 -> 네이버 모바일 로그인 페이지 이동
2. 사용자가 수동 로그인 후 터미널에서 `p` 입력
3. `KakaoTalk*.txt` 파일 중 가장 최근 파일에서 링크 추출
4. 일반 링크와 `/clip/` 링크를 분리하여 순차적으로 새 탭에서 열기
5. Chrome history 탭 열기
6. `q` 입력 시 KakaoTalk 파일 삭제 후 종료

## Development

```bash
source .venv/bin/activate
pip install -r requirements.txt
python blogAuto.py
```

## Key Notes

- 링크는 일반 링크 먼저, `/clip/` 링크 나중에 열림
- 링크 열 때 0.3~0.7초 랜덤 딜레이 적용 (봇 감지 회피)
- 중복 링크는 제거되고 정렬됨
- `KakaoTalk*.txt` 파일은 `.gitignore`에 포함 (개인정보 보호)
- 한국어 코멘트 사용
