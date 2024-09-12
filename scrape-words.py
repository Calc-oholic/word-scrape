import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# options (options.add_argument('headless'))
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# open webpage
driver.get("https://aswbee.com/Login.aspx")

# wait until box is clickable
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

word_map = {}

# looping
for test_id in range(572, 597):
    url = f"https://aswbee.com/SpellTest/Test_SelectorWordList.ashx?SpellTestID={test_id}"
    driver.get(url)

    time.sleep(.3)

    page_content = driver.find_element(By.TAG_NAME, "body").text

    try:
        word_list = json.loads(page_content)
    except json.JSONDecodeError as e:
        print(f"ERROR WITH THE JSON STUFF")
        continue

    # process for each
    for entry in word_list:
        try:
            word_id = int(entry.get("wordID", -1))
            word = entry.get("word", "").strip()

            if word_id != -1 and word:
                word_map[word] = word_id
            else:
                print(f"sad error")

        except (ValueError, TypeError) as e:
            print(f"sad error 2")

for word, word_id in sorted(word_map.items()):
    print(f"{word}:{word_id}")

driver.quit()
