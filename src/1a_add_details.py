# this processes
# `data-source/01_moma_bags_urls.tsv`
# into
# `data-source/02_moma_bags_urls_details.tsv`
# it extracts the panorama_id, ocr_id, and gsv_url using the url


import csv, re, os
from util import DATA_DIR

INPUT_FILE = os.path.join(DATA_DIR, "01_moma_bags_urls.tsv")
OUTPUT_FILE = os.path.join(DATA_DIR, "02_moma_bags_urls_details.tsv")

with open(INPUT_FILE, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    reader_list = list(reader)


########################################################
# Extract the ids from the url
########################################################


def extract_ids_from_url(url: str) -> tuple[str, str] | None:
    pattern = r"panorama/([^/?]+)\?o=(\d+)"
    match = re.search(pattern, url)
    if match:
        (panorama_id, ocr_id) = match.groups()
        return panorama_id, ocr_id
    return None


########################################################
# Scrape the gsv_url from the url
########################################################


def get_gsv_url(url: str) -> str | None:
    import requests
    from bs4 import BeautifulSoup

    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all 'a' tags with href starting with www.google.com
    google_links = soup.find_all(
        "a", href=lambda x: x and x.startswith("https://www.google.com/")
    )

    return google_links[0]["href"] if google_links else None


for row in reader_list:
    url = row["url"]
    panorama_id, ocr_id = extract_ids_from_url(url)
    row["panorama_id"] = panorama_id
    row["ocr_id"] = ocr_id

    gsv_url = get_gsv_url(url)
    row["gsv_url"] = gsv_url


# save the updated csv
with open(OUTPUT_FILE, "w") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["url", "panorama_id", "ocr_id", "notes", "gsv_url"],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(reader_list)
