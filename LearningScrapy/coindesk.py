import time
import pandas as pd
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_date():
    # wait = WebDriverWait(driver, 5)
    # parent_div = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "display-desktop-none")))
    parent_div = driver.find_element(By.XPATH, "//div[@class='display-desktop-none display-tablet-none display-mobile-none ']")
    driver.execute_script("arguments[0].setAttribute('class', 'display-desktop-block');", parent_div)
    # time.sleep(30)
    datetime_element = parent_div.find_element(By.XPATH, "//span[contains(text(), 'GMT')]")
    # datetime_element = WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'GMT')]")))
    # print(f"\n================{datetime_element.text}\n==============")
    # text = driver.execute_script("return argument[0].textContent;", datetime_element)
    return datetime_element.text



options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
driver = Chrome(options=options)
url = 'https://www.coindesk.com/tag/bitcoin/'
driver.get(url)
time.sleep(1)
driver.implicitly_wait(1)

try:
    driver.find_element(By.XPATH, "//button[@id='CybotCookiebotDialogBodyButtonDecline']").click()
except NoSuchElementException:
    pass

# for selector in driver.find_elements(By.XPATH, '//*[@id="fusion-app"]/div[2]//main/div/div/div[2]'):
pages = {
    'heading': [],
    'span_text': [],
    'datetime': []
}

while True:
    # Fetch elements on each iteration to avoid stale element reference
    headings = [heading.text for heading in driver.find_elements(By.XPATH, '//h6/a[@target="_self"]')]
    span_texts = [span.text for span in driver.find_elements(By.XPATH, '//span[@class="content-text"]')]
    datetime = get_date() #[datetime for datetime in driver.find_elements(By.XPATH, "//span[contains(text(), 'GMT')]")]

    # Extend the data dictionary lists
    pages['heading'].extend(headings)
    pages['span_text'].extend(span_texts)
    pages['datetime'].extend(datetime)

    print(pages)

    # driver.find_element(By.CLASS_NAME)
    next_page = driver.find_element(By.XPATH, "//a[@aria-label='Next page']")
    driver.execute_script("arguments[0].scrollIntoView(true);", next_page)

    # driver.implicitly_wait(3)
    actions = ActionChains(driver)
    time.sleep(1)

    if next_page:
        try:
            actions.move_to_element(next_page).click().perform()
            # next_page.click()
        except (ElementClickInterceptedException, NoSuchElementException) as e:
            print(f'stuck at {next_page}')
            break

news_data = pd.DataFrame(pages)
news_data.to_csv('coindesk.csv')

print(news_data)






# //span[@class="content-text"]

