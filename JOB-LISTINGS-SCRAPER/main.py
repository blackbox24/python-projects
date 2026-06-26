import requests
import logging
import csv
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("job_listings")

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

data = [
    ["Title","Location","Company name","Job URL"],
]
if response.status_code == 200:
    content = response.content
    logger.info("successful")
    html = BeautifulSoup(content, 'html.parser')
    
    # job title
    # company name
    # location
    # job detail url
    cards = html.find_all("div", "card") # type: ignore
    for card in cards:
        card_content = card.find("div","content")
        media_content = card.find("div","media-content")
        footer = card.find("footer","card-footer")

        # job title
        title = media_content.find("h2", "title")

        # location
        location = card_content.find("p","location")

        # company name
        company = media_content.find("h3","company")

        # job detail url
        job_url = footer.a["href"]

        jobDetail = [
            title.string.strip(),
            location.string.strip(),
            company.string,
            job_url
        ]

        data.append(jobDetail)
    
    with open("jobs.csv","w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


else:
    logger.error("failed, status code: " + str(response.status_code))