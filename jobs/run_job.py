import logging
from services.test_browser_service import run_automation
# import os

# Ensure logs folder exists
# os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/job.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    try:
        run_automation()
    except Exception as e:
        logging.exception(f"Job failed: {str(e)}")