import time
import json
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# ==============================
# CONFIG
# ==============================

CSV_FILE = r"C:\Users\dell\Downloads\Location_IDs.csv"
OUTPUT_JSON = r"C:\Users\dell\Downloads\plugshare_full_data.json"
SAVE_INTERVAL = 20
DRIVER_PATH = r"C:\Users\dell\Downloads\uc_driver_temp\chromedriver.exe"


# ==============================
# DRIVER SETUP
# ==============================

chrome_options = Options()
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--start-maximized")

service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)


# ==============================
# POPUP BYPASS
# ==============================

def close_popup():

    try:
        close_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
        close_btn.click()
        return
    except:
        pass

    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
    except:
        pass

    driver.execute_script("""
        document.querySelectorAll('[role="dialog"]').forEach(e => e.remove());
        document.querySelectorAll('.ReactModal__Overlay').forEach(e => e.remove());
        document.querySelectorAll('.ReactModalPortal').forEach(e => e.remove());
        document.body.style.overflow = "auto";
    """)


# ==============================
# CLEAR OLD LOGS
# ==============================

def clear_logs():
    driver.get_log("performance")


# ==============================
# GET FULL API JSON
# ==============================

def get_api_json(location_id):

    logs = driver.get_log("performance")

    for log in logs:

        message = json.loads(log["message"])["message"]

        if message["method"] == "Network.responseReceived":

            url = message["params"]["response"]["url"]

            if f"locations/{location_id}" in url:

                request_id = message["params"]["requestId"]

                try:
                    body = driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": request_id}
                    )

                    return json.loads(body["body"])

                except:
                    pass

    return None


# ==============================
# SCRAPE FUNCTION
# ==============================

def scrape_location(location_id):

    url = f"https://www.plugshare.com/location/{location_id}"
    print(f"Scraping → {location_id}")

    clear_logs()

    driver.get(url)
    time.sleep(4)

    driver.execute_script(
        'localStorage.setItem("ps_signup_prompt_seen", "true");'
    )

    time.sleep(3)

    close_popup()

    time.sleep(4)

    data = get_api_json(location_id)

    if isinstance(data, list):
        data = data[0]

    return data


# ==============================
# LOAD CSV
# ==============================

df = pd.read_csv(CSV_FILE)
location_ids = df.iloc[:, 0].dropna().tolist()


# ==============================
# LOAD PREVIOUS DATA (Resume)
# ==============================

results = []

try:
    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        results = json.load(f)
except:
    results = []


# ==============================
# SCRAPING LOOP
# ==============================

counter = 0

for loc_id in location_ids:

    try:
        data = scrape_location(loc_id)

        if data:
            results.append(data)
            counter += 1

    except Exception as e:
        print(f"Error → {loc_id} : {e}")

    # ⭐ SAVE EVERY 20 RECORDS
    if counter >= SAVE_INTERVAL:

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print("💾 Auto Saved 20 Records")
        counter = 0

    time.sleep(2)


# ==============================
# FINAL SAVE
# ==============================

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

driver.quit()

print("✅ Scraping Completed")
