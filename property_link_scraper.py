import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Create the ChromeDriver service
service = Service('~/Git/chromedriver/')
options = webdriver.ChromeOptions().add_argument('--incognito')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def get_page_link(state, page_no):
    return f"https://www.domain.com.au/sale/?sort=dateupdated-desc&state={state}&page={page_no}"


for i in range(1, 51):
    # Navigate to the website
    # driver.get('https://www.realestate.com.au/buy/in-vic/list-1')
    driver.get(get_page_link("vic", i))

    property_page = driver.find_elements(By.XPATH, '//a[contains(@class, "address is-two-lines")]')

    for prty in property_page:
        link = prty.get_attribute("href")
        print(link)
        f = open("property_links.txt", "a")
        f.write(link + "\n")
        f.close()

    time.sleep(5)
# Find all article title elements
# property_page = driver.find_element(By.XPATH, '//div[@class="divided-content"]')
# property_page = driver.find_elements(By.XPATH, '//ul[@data-testid="results"]/li')

# property_page = driver.find_element(By.CSS_SELECTOR, "ul[data-testid='results']")
# prty_list = property_page.find_elements(By.TAG_NAME, 'li')
# if py_list: print(list.count(py_list))
# Extract and print the text of each title


# Close the browser
driver.quit()
