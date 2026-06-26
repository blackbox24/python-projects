import requests
from typing import Optional
import logging
import csv
from bs4 import BeautifulSoup, Tag

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("job_listings")

TARGET_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "jobs.csv"
CSV_HEADERS = ["Title","Location","Company name","Job URL"]
REQUEST_TIMEOUTS = 10

def fetch_page_content(url:str) -> Optional[bytes]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Successfully fetch the webpage")
        return response.content
    except Exception as e:
        logger.error(f"Error: {e}")

    return None

def parse_job_card(card: Tag) -> Optional[list[str]]:
    card_content = card.find("div","content") # type: ignore
    media_content = card.find("div","media-content") # type: ignore
    footer = card.find("footer","card-footer") # type: ignore

    if not(card_content and media_content and footer):
        return None
    
    title_el =  media_content.find("h2", "title")

    # location
    location_el = card_content.find("p","location")

    # company name
    company_el = media_content.find("h3","company")

    # job detail url
    link_el = footer.find("a")

    title = title_el.get_text(strip=True) if title_el else "N/A"
    location = location_el.get_text(strip=True) if location_el else "N/A"
    company = company_el.get_text(strip=True) if company_el else "N/A" 

    job_url = "N/A"

    if link_el and link_el.has_attr("href"):
        job_url = link_el["href"].strip()

    return [title, location, company, job_url]


def save_to_csv(filepath: str, headers: list[str], records: list[list[str]]) -> None:
    try:
        with open(filepath, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(records)
        logger.info("Successfully wrote %d jobs to %s", len(records), filepath)
    except Exception as e:
        logger.error("Error: "+str(e))

def main():
    raw_html = fetch_page_content(TARGET_URL)

    if raw_html is None:
        return
    
    soup = BeautifulSoup(raw_html, "html.parser")
    job_cards = soup.find_all("div", class_="card")

    if job_cards is None:
        logger.warning("No jobs cards found on the page")
        return 
    parse_jobs:list[list[str]] = [] 
    
    for card in job_cards:
        data = parse_job_card(card)
        if data:
            parse_jobs.append(data)

    if parse_jobs:
        save_to_csv(OUTPUT_FILE, CSV_HEADERS, parse_jobs)

    else:
        logger.warning("No valid job information could be parsed from the page.")


if __name__ == "__main__":
    main()