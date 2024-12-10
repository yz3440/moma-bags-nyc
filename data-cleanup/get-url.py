import pandas as pd


df = pd.read_csv("panorama_urls.csv")

# print all the ocr_ids
print(df["ocr_id"].unique())

exit()


def get_website_data(url):
    import requests
    from bs4 import BeautifulSoup

    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all 'a' tags with href starting with www.google.com
    google_links = soup.find_all(
        "a", href=lambda x: x and x.startswith("https://www.google.com/")
    )

    displayed_address = soup.find("p", string=lambda x: x and "United States" in x)

    # Print the found links
    return {
        "gsv_url": google_links[0]["href"],
        "displayed_address": displayed_address.text if displayed_address else None,
    }


def get_website_data_from_url(url):
    return get_website_data(url)


# Create a new column for Google URLs
df["gsv_url"] = df["url"].apply(get_gsv_url)

# recorder the column names
# from url,panorama_id,ocr_id,notes,gsv_url
# to gsv_url, url,panorama_id,ocr_id,notes

# remove the quotes from the gsv_url
# Remove quotes from gsv_url column, handling NaN values
df["gsv_url"] = df["gsv_url"].fillna("").astype(str).str.replace('"', "")


df = df[["gsv_url", "url", "panorama_id", "ocr_id", "notes"]]
# Save the updated dataframe to a new CSV file
df.to_csv("panorama_urls_with_gsv.tsv", index=False, quoting=None, sep="\t")
