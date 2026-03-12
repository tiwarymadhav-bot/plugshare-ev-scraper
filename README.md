# ⚡ PlugShare EV Charger Data Scraper

A production-grade Python scraper that extracts **EV charging station data** from [PlugShare](https://www.plugshare.com) using **Selenium + Chrome DevTools Protocol (CDP) Network Interception**.

---

## 🚀 Features

- 🔍 **CDP Network Interception** — Captures live API responses directly from browser network logs (no HTML parsing needed)
- 🤖 **Smart Popup Bypass** — Auto-closes login/signup popups using 3 fallback methods
- 💾 **Auto-Save every 20 records** — Prevents data loss on crashes
- 🔄 **Resume Support** — Picks up from where it left off using existing output file
- 📦 **Bulk Processing** — Reads thousands of Location IDs from a CSV file
- 🧹 **Clean JSON Output** — Structured, indented, ready for analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Selenium | Browser automation |
| Chrome CDP | Network log interception |
| Pandas | CSV input handling |
| JSON | Output format |

---

## 📁 Project Structure

```
plugshare-scraper/
│
├── ev_charger_scraper_network.py   # Main scraper script
├── Location_IDs.csv                # Input: list of PlugShare location IDs
├── plugshare_full_data.json        # Output: scraped data
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/tiwarymadhav-bot/plugshare-ev-scraper.git
cd plugshare-ev-scraper
```

### 2. Install dependencies
```bash
pip install selenium pandas
```

### 3. Download ChromeDriver
- Download from: https://chromedriver.chromium.org/downloads
- Match your Chrome browser version
- Update `DRIVER_PATH` in the script

### 4. Prepare your input CSV
- Create a CSV file with Location IDs in the first column
- Update `CSV_FILE` path in the script

---

## 🔧 Configuration

Edit these variables at the top of the script:

```python
CSV_FILE      = "path/to/Location_IDs.csv"
OUTPUT_JSON   = "path/to/output.json"
SAVE_INTERVAL = 20           # Save after every N records
DRIVER_PATH   = "path/to/chromedriver.exe"
```

---

## ▶️ Usage

```bash
python ev_charger_scraper_network.py
```

The script will:
1. Load Location IDs from CSV
2. Open each PlugShare location in Chrome
3. Intercept the API response via CDP
4. Save data to JSON every 20 records
5. Auto-resume if restarted

---

## 📊 Sample Output

```json
{
    "id": 123456,
    "name": "Tesla Supercharger - Downtown",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "plugs": [...],
    "checkins": [...],
    "address": "123 Main St, San Francisco, CA"
}
```

---

## 💡 How It Works

Traditional scrapers parse HTML — but PlugShare loads data dynamically via API calls. This scraper intercepts those API calls directly using **Chrome DevTools Protocol**, capturing the full JSON payload without any fragile HTML parsing.

```
Browser loads page
    ↓
API call fires in background
    ↓
CDP captures network response
    ↓
Script extracts & saves JSON
```

---

## 📌 Use Cases

- EV infrastructure research & analysis
- Charging network density mapping
- Data for ML models on EV adoption
- Business intelligence for charging operators

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Always review a website's Terms of Service before scraping. The author is not responsible for any misuse.

---

## 👨‍💻 Author

**Madhav Tiwary**
Python Developer | Web Scraping & Data Engineering
- 📧 Tiwarymadhav.gmail.com
- 💼 [[Upwork/Contra profile link]](https://www.upwork.com/freelancers/~01f57d319968afb3a8?mp_source=share)


---

## ⭐ If this project helped you, give it a star!
