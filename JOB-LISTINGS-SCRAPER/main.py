import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("job_listings")

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

if response.status_code == 200:
    content = response.content
    print(content)
    logger.info("successful")

else:
    logger.error("failed, status code: " + str(response.status_code))