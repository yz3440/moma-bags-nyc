# this joins
# `data-source/02_moma_bags_urls_details.tsv`
# and
# `data-source/03_moma_bags_db_dump.tsv`
# into
# `data-source/04_moma_bags_complete.tsv`


import pandas as pd
import os
from util import DATA_DIR

path_1 = os.path.join(DATA_DIR, "02_moma_bags_urls_details.tsv")
path_2 = os.path.join(DATA_DIR, "03_moma_bags_db_dump.tsv")

df_1 = pd.read_csv(path_1, sep="\t")
df_2 = pd.read_csv(path_2, sep="\t")

df = pd.merge(df_1, df_2, on="ocr_id")

df = df[
    [
        "gsv_url",
        "url",
        "ocr_id",
        "yaw",
        "pitch",  # the first pitch is coordinate of the text in the image
        "width",
        "height",
        "panorama_id_x",
        "notes",
        "lat",
        "lon",
        "copyright",
        "date",
        "heading",
        "pitch.1",  # the second pitch is the original pitch offset of the 360 camera
        "roll",
        "displayed_address",
        "suburb",
    ]
]


# rename the columns
df.rename(
    columns={
        "yaw": "ocr_yaw",
        "pitch": "ocr_pitch",
        "width": "ocr_width",
        "height": "ocr_height",
        "panorama_id_x": "panorama_id",
        "pitch.1": "pitch",
    },
    inplace=True,
)


df.to_csv(
    os.path.join(DATA_DIR, "04_moma_bags_complete.tsv"),
    sep="\t",
    index=False,
)
