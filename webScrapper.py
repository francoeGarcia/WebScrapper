from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

site = 'https://www.nike.com/w/mens-best-76m50znik1'
path = '/Users/franc/OneDrive/Documentos/chromedriver-win64/chromedriver.exe'

models = []
prices = []

service = Service(executable_path=path)
service.page_load_strategy = 'normal'
driver = webdriver.Chrome(service=service)
driver.get(site)

try:
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "css-1t0asop") and contains(@data-testid,"product-card")]')))
    data = driver.find_elements(By.XPATH, '//div[contains(@class, "css-1t0asop") and contains(@data-testid,"product-card")]')    
    for item in data:
        try:
            # check if element meet criteria before proceeding
            model_element = item.find_element(By.XPATH, ".//div[@class='product-card__title' and @role='link']")
            if model_element:
                model = model_element.text
                price_element = item.find_element(By.XPATH, './/div[contains(@data-testid, "product-price")]')
                price = price_element.text
                models.append(model)
                prices.append(price)
            else:
                # if element doesn't meet criteria, skip 
                continue
        except Exception as e:
            print(f"ERROR occurred while processing element: {e}")
    
    df = pd.DataFrame({'Nike Best Selling Shoes -> Product Name': models, 'Price': prices})
    df.to_csv('sneakers.csv', index=False, encoding='utf-8')

except Exception as e:
    print(f"Error occurred: {e}\nhere\n")

finally:
    # quit driver, close everything down
    driver.quit()