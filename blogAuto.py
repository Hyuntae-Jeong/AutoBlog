# python 3.11.9
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import glob

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

    try:
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

    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please make sure it exists.")
        return [], []

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

def keep_browser_open():
    """
    브라우저를 계속 열어두고, 'q' 입력 시 KakaoTalk 파일 삭제 후 종료
    """
    try:
        print("Browser will remain open.")
        print("Type 'q' and press Enter to delete KakaoTalk files and exit.")
        print("Press Enter to keep the browser open, or Ctrl+C to close manually.")
        while True:
            user_input = input("Enter command: ").strip().lower()
            if user_input == 'q':
                print("Detected 'q'. Deleting KakaoTalk files and exiting program.")
                delete_kakao_files()  # KakaoTalk 파일 삭제
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
    keep_browser_open()