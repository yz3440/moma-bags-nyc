import re
import csv
from io import StringIO


def extract_url_parts(urls_text):
    # Regular expression to extract ID and order number
    pattern = r"panorama/([^/?]+)\?o=(\d+)"

    # Process each line
    data = []
    for line in urls_text.strip().split("\n"):
        # Extract just the URL from markdown format [URL](URL)
        url_match = re.search(r"\[(.*?)\]", line)
        if url_match:
            url = url_match.group(1)
            # Remove any additional notes like "(hat)"
            url = url.split(" ")[0]

            match = re.search(pattern, url)
            if match:
                panorama_id, order_num = match.groups()
                data.append(
                    [
                        url,  # Full URL
                        panorama_id,  # Panorama ID
                        order_num,  # Order number
                    ]
                )

    return data


def create_csv(data):
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["URL", "Panorama_ID", "Order_Number"])

    # Write data rows
    writer.writerows(data)

    return output.getvalue()


# Example usage:
with open("bag.txt", "r") as f:
    urls_text = f.read()
data = extract_url_parts(urls_text)
csv_output = create_csv(data)

# Print the CSV content
print(csv_output)

# To save to a file:
with open("panorama_urls.csv", "w", newline="") as f:
    f.write(csv_output)
