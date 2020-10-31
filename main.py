from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import zipfile
import subprocess
import time
import argparse

LMS_login_url = "https://lms.iust.ac.ir/login/index.php"


def login(username, password, driver):
    global LMS_login_url
    driver.get(LMS_login_url)
    driver.find_element_by_link_text("ورود به سامانه مدیریت یادگیری (سامیا)").click()
    driver.find_element_by_id("edit-name").send_keys(username)
    driver.find_element_by_id("edit-pass").send_keys(password)
    driver.find_element_by_id("edit-submit").click()
    print(driver.title)
    return driver


def setup_driver():
    profile = webdriver.FirefoxProfile()

    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), "downloads"))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = True
    return webdriver.Firefox(firefox_profile=profile, capabilities=cap)


def load_class(url, driver, path):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    print(driver.title)
    wait.until(EC.url_contains("connect.iust.ac.ir"))
    class_url = driver.current_url
    idx = 3
    if class_url[:4] != "http":
        print("not http")
        idx = 1
    class_id = class_url.split('/')[idx]
    download_url = f"https://connect.iust.ac.ir/{class_id}/output/{class_id}.zip?download=zip"

    if os.path.isfile(os.path.join(path, f"{class_id}.zip")):
        print("File already exists in the download folder, Do you want to replace it? (y)es/(n)o")
        while True:
            command = input()
            command = command.lower()
            if command == 'y' or command == 'yes':
                os.remove(os.path.join(path, f"{class_id}.zip"))
                break
            elif command == 'n' or command == 'no':
                print("Abort, Exiting...")
                exit(0)
            else:
                print("Invalid command, Use y/n")

    print("downloading file...")
    driver.set_page_load_timeout(2)
    try:
        driver.get(download_url)
    except:
        pass
    print(os.path.join(path, f"{class_id}.zip"))
    while not os.path.isfile(os.path.join(path, f"{class_id}.zip")) or os.path.isfile(os.path.join(path, f"{class_id}.zip.part")):
        time.sleep(1)
        print("shit")
        pass

    print("Download finished.")
    return f"{class_id}.zip"


def unzip(path, zip_name):
    file_path = os.path.join(path, zip_name)

    if not os.path.exists(os.path.join(path, zip_name.split('.')[0])):
        os.mkdir(os.path.join(path, zip_name.split('.')[0]))
    extract_path = os.path.join(path, zip_name.split('.')[0])

    with zipfile.ZipFile(file_path, 'r') as f:
        f.extractall(extract_path)

    return extract_path


def find_video_files(path):
    files = os.listdir(path)

    pairs = []
    for file in files:
        location = os.path.join(path, file)
        size = os.path.getsize(location)
        pairs.append((size, file))

    pairs.sort(key=lambda s: s[0])
    print(pairs)
    video_file = os.path.join(path, pairs[-1][1])
    sound_file = os.path.join(path, pairs[-2][1])

    return video_file, sound_file


def export_video(video_path, sound_path, unzipped_path):
    """
    ffmpeg -i cameraVoip_1_11.flv -i screenshare_2_10.flv -c copy -map 0:a:0 -map 1:v:0 -shortest output.flv
    """
    print(video_path)
    print(sound_path)
    save_path = os.path.join(unzipped_path, "final_video.flv")
    commands = ['ffmpeg', '-i', sound_path, '-i', video_path, '-c', 'copy', '-map', '0:a:0', '-map', '1:v:0',
                '-shortest', save_path]
    subprocess.call(commands)
    print(f"Video was saved to {save_path}")


if __name__ == '__main__':

    print("Enter your LMS username:")
    username = input()
    print("Enter your LMS password:")
    password = input()
    print("Enter the url of the video:")
    url = input()

    driver = setup_driver()
    driver.delete_all_cookies()
    if not os.path.exists(os.path.join(os.getcwd(), "downloads")):
        print(os.path.join(os.getcwd(), "downloads"))
        os.mkdir("downloads")

    path = os.path.join(os.getcwd(), "downloads")

    driver = login(username, password, driver)

    zip_name = load_class(url, driver, path)

    unzipped_path = unzip(path, zip_name)

    video_file, sound_file = find_video_files(unzipped_path)

    export_video(video_file, sound_file, unzipped_path)
