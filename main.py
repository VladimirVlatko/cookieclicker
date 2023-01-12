from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(3)

lang = driver.find_element(By.ID, "langSelect-EN")
lang.click()

cookie = driver.find_element(By.ID, "bigCookie")

# Create a list with the products from the store
def list_product_prices():
    all_products = []
    for num in range(0, 9):
        product = driver.find_element(By.CSS_SELECTOR, f"#productPrice{num}")
        if product.text != "":
            new_product = product.text.replace(",", "").replace(".", "").strip("million")
            all_products.append(int(new_product))
    return all_products

# Check which upgrades are affordable and purchase the most expensive one
def buy_product():
    num_of_cookies = int(driver.find_element(By.ID, "cookies").text.split(" ")[0].replace(",", ""))
    products_list = list_product_prices()
    green_products = []
    for product in products_list:
        if num_of_cookies >= product:
            green_products.append(product)
    if len(green_products) > 1:
        product_to_buy = driver.find_element(By.ID, f"product{len(green_products) - 1}")
        product_to_buy.click()


start = time.time()
end_after = 180
check_after = 5

time.sleep(2)
# Start the bot
while True:
    delta = time.time() - start
    cookie.click()
    if delta >= check_after:
        buy_product()
        check_after += 5
    if delta >= end_after:
        per_second = driver.find_element(By.ID, "cookiesPerSecond").text
        print("Cookies " + per_second)
        break

driver.quit()
