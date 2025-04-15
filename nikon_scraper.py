import requests
from bs4 import BeautifulSoup
import yaml
import time
import os
from datetime import datetime
import pytz
import json

def load_urls(file_path):
    with open(file_path, 'r') as f:
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            data = yaml.safe_load(f)
            return list(data.values())
        else:
            return [line.strip() for line in f if line.strip()]

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_stock(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = {
        "url": url,
        "stock_status": "Unknown",
        "sale_price": None,
        "original_price": None,
        "you_save": None,
        "discount_label": None,
        "calculated_discount_pct": None
    }

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "AddToCart_add-to-cart__JiSYP"))
        )
        time.sleep(1)  # Give time for JS to fully render

        # Check stock status
        button = driver.find_element(By.CLASS_NAME, "AddToCart_add-to-cart__JiSYP").find_element(By.TAG_NAME, "button")
        button_text = button.text.strip().upper()
        is_disabled = not button.is_enabled()
        data["stock_status"] = "Out of Stock" if "OUT OF STOCK" in button_text or is_disabled else "In Stock"

        # Extract prices
        try:
            sale_price = driver.find_element(By.CLASS_NAME, "ProductInformation_price__87FVE").text.replace("$", "").replace(",", "")
            data["sale_price"] = float(sale_price)
        except:
            pass

        try:
            original_price = driver.find_element(By.CLASS_NAME, "ProductInformation_price-was__ttV5P").text.replace("$", "").replace(",", "")
            data["original_price"] = float(original_price)
        except:
            pass

        try:
            savings = driver.find_element(By.CLASS_NAME, "ProductInformation_you-save__U4kqR").text
            savings = savings.replace("You Save", "").replace("$", "").replace(",", "").strip()
            data["you_save"] = float(savings)
        except:
            pass

        try:
            label = driver.find_element(By.CLASS_NAME, "ProductDiscountDescriptions_discount__Q8D_3").text
            data["discount_label"] = label
        except:
            pass

        # Calculate discount percentage
        if data["sale_price"] and data["original_price"]:
            pct = (1 - data["sale_price"] / data["original_price"]) * 100
            data["calculated_discount_pct"] = round(pct, 2)

    except Exception as e:
        data["stock_status"] = f"Error: {e}"

    finally:
        driver.quit()
        return data

def check_stock_with_retry(url, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            return check_stock(url)  # Call your existing check_stock function
        except Exception as e:
            attempt += 1
            if attempt == retries:
                return {"url": url, "stock_status": f"Error: {e}"}
            time.sleep(uniform(delay, delay + 2))  # Exponential backoff or random sleep

def main():
    input_file = os.getenv("URLS_FILE", "urls.yaml")
    urls = load_urls(input_file)

    results = []
    print(f"Checking {len(urls)} URLs...")

    for url in urls:
        # Use retry mechanism here
        info = check_stock_with_retry(url)
        results.append(info)
        print(info)  # You could also log this to a file
        time.sleep(1)  # Be polite with Nikon's servers

    eastern = pytz.timezone("US/Eastern")
    timestamp = datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S %Z")

    # Restructure and enrich results before writing
    logged_data = []
    for item in results:
        logged_item = {
            "url": item.get("url"),
            "timestamp": timestamp,
            "stock_status": item.get("stock_status"),
            "sale_price": item.get("sale_price"),
            "original_price": item.get("original_price"),
            "you_save": item.get("you_save"),
            "discount_label": item.get("discount_label"),
            "calculated_discount_pct": item.get("calculated_discount_pct")
        }
        logged_data.append(logged_item)

    # Function to handle appending to the JSON file or creating a new one
    def append_to_json(file_path, data):
        if os.path.exists(file_path):
            # If file exists, read the existing data
            with open(file_path, "r") as f:
                existing_data = json.load(f)
            # Append the new data to the existing data
            existing_data.extend(data)
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=2)
        else:
            # If file doesn't exist, create it and write the data
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

    # Now use the append_to_json function in your main code
    append_to_json("product_status_log.json", logged_data)

if __name__ == "__main__":
    main()