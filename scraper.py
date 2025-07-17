import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def scrape_amazon(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.amazon.in")

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    products = []
    for page in range(1, 10):
        time.sleep(2)
        items = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]')
        for item in items:
            try:
                name = item.find_element(By.TAG_NAME, "h2").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                price_elem = item.find_element(By.CSS_SELECTOR, ".a-price-whole")
                price = price_elem.text if price_elem else "N/A"
                products.append({"Name": name, "Price": price, "Link": link})
            except:
                continue
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
            driver.execute_script("arguments[0].click();", next_btn)
        except:
            break

    driver.quit()
    
    df = pd.DataFrame(products)
    filename = f"{search_term.replace(' ', '_')}_products.csv"
    filepath = os.path.join("static", filename)
    df.to_csv(filepath, index=False)
    return filename, len(products)
