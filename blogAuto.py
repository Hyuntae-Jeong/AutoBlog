# python 3.11.9
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import glob
import csv

site_url = 'https://nid.naver.com/nidlogin.login?svctype=262144&url=http://undefined/aside/'    #네이버 모바일 로그인 URL
history_url = 'chrome://history/'    #Chrome history URL

#크롬 실행
def exec_chrom():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def wait_for_user_to_login(driver):
    """
    네이버 로그인 페이지를 열고 사용자가 직접 로그인하도록 대기
    """
    driver.get(site_url)
    print("Please log in manually in the browser.")
    print("After logging in, type 'p' and press Enter in the Python terminal to continue.")

    while True:
        user_input = input("Enter 'p' to continue: ").strip().lower()
        if user_input == 'p':
            print("Detected 'p'. Proceeding to the next step.")
            break
        print("Invalid input. Please type 'p' and press Enter after logging in.")

def detect_kakao_format(file_path):
    """
    KakaoTalk 내보내기 파일의 포맷을 첫 2줄만 읽고 판별.
    :param file_path: 검사할 파일 경로
    :return: "mac" (CSV 형식) 또는 "windows" (plain-text 형식)
    :raises ValueError: 두 포맷 모두 매치되지 않을 때 (지원하지 않는 형식)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().rstrip('\n')
        second_line = file.readline().rstrip('\n')

    if first_line.startswith("Date,User,Message"):
        return "mac"
    if "최적화 톡방" in first_line and second_line.startswith("저장한 날짜 :"):
        return "windows"
    raise ValueError(f"지원하지 않는 KakaoTalk 파일 포맷입니다: {file_path}")


def parse_kakao_messages(file_path, fmt):
    """
    KakaoTalk 내보내기 파일을 (사용자, 내용) 튜플 리스트로 파싱.
    URL 추출/필터링은 호출자의 책임. 이번 단계에서는 메시지 단위로만 정규화.
    :param file_path: 파일 경로
    :param fmt: "mac" 또는 "windows" (detect_kakao_format()의 반환값)
    :return: [(user, content), ...] 등장 순서 보존
    :raises ValueError: 알 수 없는 fmt 값
    """
    messages = []
    if fmt == "mac":
        # csv 모듈이 따옴표 처리/콤마 이스케이프를 알아서 해줘서 URL 끝 따옴표 회귀 차단
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Date,User,Message 헤더 스킵
            for row in reader:
                if len(row) >= 3:
                    messages.append((row[1], row[2]))
        return messages
    if fmt == "windows":
        # 메시지 라인 형식: [사용자명] [오전/오후 H:MM] 내용
        pattern = re.compile(r'^\[(.+?)\] \[(?:오전|오후) \d{1,2}:\d{2}\] (.*)$')
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines[2:]:  # 1·2번째 줄(헤더) 스킵
            line = line.rstrip('\n')
            if not line.strip():
                continue  # 빈 줄 스킵 (헤더 다음 + 그 외)
            m = pattern.match(line)
            if m:
                messages.append((m.group(1), m.group(2)))
            # 매치 실패하면 섹션 헤더(--------- … ---------)이거나 멀티라인 잔여물 — 스킵
        return messages
    raise ValueError(f"알 수 없는 포맷: {fmt!r}")


def extract_links_from_kakao():
    """
    'KakaoTalk'로 시작하는 텍스트 파일에서 링크를 추출하고,
    '/clip/'이 포함된 링크와 그렇지 않은 링크를 분리하는 함수
    :return: 일반 링크 리스트, '/clip/' 링크 리스트
    """
    files = glob.glob("KakaoTalk*.txt")
    if not files:
        print("No 'KakaoTalk' files found in the current directory.")
        return [], []

    file_name = max(files, key=os.path.getmtime)
    print(f"Reading file: {file_name}")

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    general_links = []
    clip_links = []

    for line in lines:
        match = re.search(r'https?://[^\s]+', line)
        if match:
            link = match.group()
            if '/clip/' in link:
                clip_links.append(link)  # '/clip/' 링크 저장
            else:
                general_links.append(link)  # 일반 링크 저장

    general_links = sorted(set(general_links))
    clip_links = sorted(set(clip_links))

    return general_links, clip_links

def open_link(driver, link_list, delay=True):
    """
    추출된 링크들을 새 탭에서 차례로 열기
    :param driver: 웹드라이버
    :param link_list: 링크 리스트
    :param delay: 대기 시간 사용 여부
    """
    for site in link_list:
        driver.execute_script(f"window.open('{site}', '_blank');")
        if delay:
            time.sleep(random.uniform(0.3, 0.7))  # 랜덤 대기

def open_history_tab(driver):
    """
    마지막에 Chrome history 탭 열기
    """
    driver.switch_to.new_window('tab')
    driver.get(history_url)
    print("\nOpened Chrome history tab.")

def delete_kakao_files():
    """
    현재 디렉토리에서 'KakaoTalk'로 시작하는 모든 .txt 파일을 삭제
    """
    files = glob.glob("KakaoTalk*.txt")
    if not files:
        print("No 'KakaoTalk' files found to delete.")
    else:
        for file in files:
            try:
                os.remove(file)
                print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

def keep_browser_open(driver):
    """
    브라우저를 계속 열어두고, 'q' 입력 시 KakaoTalk 파일 삭제 및 드라이버/브라우저 종료
    """
    try:
        print("Browser will remain open.")
        print("Type 'q' and press Enter to delete KakaoTalk files, close the browser, and exit.")
        while True:
            user_input = input("Enter command: ").strip().lower()
            if user_input == 'q':
                print("Detected 'q'. Deleting KakaoTalk files and closing the browser.")
                delete_kakao_files()  # KakaoTalk 파일 삭제
                driver.quit()  # 드라이버 정리 및 크롬 창 닫기
                break  # 루프 종료
            print("Keeping the browser open.")
    except KeyboardInterrupt:
        print("Exiting program. Browser will not be closed.")


# 메인 실행 부분 수정
if __name__ == '__main__':
    driver = exec_chrom()
    wait_for_user_to_login(driver)

    # 링크 추출 및 분리
    general_links, clip_links = extract_links_from_kakao()

    if general_links or clip_links:
        print("Extracted Links:")
        print("\n[General Links]")
        for link in general_links:
            print(link)
        print("\n[Clip Links]")
        for link in clip_links:
            print(link)
    else:
        print("No links found or no valid files.")

    print("General link count: ", len(general_links))
    print("Clip link count: ", len(clip_links))

    # 일반 링크 먼저 열기
    print("\nOpening general links...")
    open_link(driver, general_links)

    # '/clip/' 링크 나중에 열기
    print("\nOpening '/clip/' links...")
    open_link(driver, clip_links)

    # 마지막에 history 탭 열기
    open_history_tab(driver)

    # 브라우저 유지
    keep_browser_open(driver)