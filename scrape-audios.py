import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

download_dir = os.path.abspath('pronunciations')
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

driver.get("https://aswbee.com/Login.aspx")

wait = WebDriverWait(driver, 10)
team_name_box = wait.until(EC.element_to_be_clickable((By.ID, "content_txtTeamName")))
team_name_box.send_keys("Spelling Tests")
username_box = wait.until(EC.element_to_be_clickable((By.ID, "content_txtLoginName")))
username_box.send_keys("asingh")
password_box = wait.until(EC.element_to_be_clickable((By.ID, "content_txtPassword")))
password_box.send_keys("eagles")
login_button = wait.until(EC.element_to_be_clickable((By.ID, "content_btnLogin")))
login_button.click()

wait.until(EC.url_contains("SpellTest"))
word_to_id = {}
with open('links.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            try:
                word_list_num, word_id = line.split(':')
                word_to_id[word_id] = word_list_num
            except ValueError:
                print(f"Error processing line: {line}")

for word_id, word_list_num in word_to_id.items():
    url = f"https://aswbee.com/SpellTest/Test_WordAudio.ashx?WordID={word_id}&v=0"
    file_name = f"{word_list_num}.mp3"

    try:
        driver.get(url)
        time.sleep(.1)

        # Javascript anchor tags????
        driver.execute_script('''
            let aLink = document.createElement("a");
            aLink.href = arguments[0];
            aLink.download = arguments[1];
            document.body.appendChild(aLink);
            aLink.click();
            aLink.remove();
        ''', url, file_name)
        print(f"Triggered download for {file_name}")

        time.sleep(.1)

    except Exception as e:
        print(f"Error downloading {url}: {e}")

driver.quit()
