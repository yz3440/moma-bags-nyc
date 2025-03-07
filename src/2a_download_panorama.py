from streetlevel import streetview
import os, csv
from util import ASSETS_DIR, DATA_DIR

DATA = os.path.join(DATA_DIR, "04_moma_bags_complete.tsv")


with open(DATA, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    reader_list = list(reader)


for row in reader_list:
    pano_id = row["panorama_id"]
    try:
        pano = streetview.find_panorama_by_id(pano_id)
        panorama_pil_image = streetview.get_panorama(pano=pano)
        panorama_pil_image.save(os.path.join(ASSETS_DIR, f"{pano_id}.jpg"))
    except Exception as e:
        print(f"Error downloading panorama {pano_id}")
