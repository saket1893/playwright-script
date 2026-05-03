from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# locators for the Market Data menu and Equity link
MARKET_DATA_MENU = 'a#link_2.nav-link.dd-link'
EQUITY_SME_MARKET_LINK = 'a.nav-link[href="/market-data/live-equity-market"]'

# locators for the CSV download button with specific HTML path structure
# HTML: <div class="downloads"><ul><li><a href="#" id="dnldEquityStock">...
DOWNLOAD_CSV_BUTTON = 'a#dnldEquityStock'  # Direct anchor by ID
DOWNLOAD_CSV_BUTTON_ALT_1 = 'div.downloads li a#dnldEquityStock'  # Full path to anchor
DOWNLOAD_CSV_BUTTON_ALT_2 = 'div.downloads ul li a[id="dnldEquityStock"]'  # Alternative path
DOWNLOAD_CSV_BUTTON_ALT_3 = 'div.downloads a'  # Generic downloads link
DOWNLOAD_CSV_BUTTON_ALT_4 = 'a#dnldEquityStock img'  # Image inside anchor
DOWNLOAD_CSV_BUTTON_ALT_5 = 'span#dwldcsv'  # Span text inside anchor

# download target paths
CSV_DOWNLOAD_PATH = DATA_DIR / "equity_market.csv"
EXCEL_DOWNLOAD_PATH = DATA_DIR / "equity_market.xlsx"


