from streetlevel import streetview
import os, csv, numpy as np
from PIL import Image
from util import ASSETS_DIR, DATA_DIR, e2p

DATA = os.path.join(DATA_DIR, "04_moma_bags_complete.tsv")


panorama_dir = os.path.join(ASSETS_DIR, "panorama")
perspective_image_dir = os.path.join(ASSETS_DIR, "perspective_image")
os.makedirs(panorama_dir, exist_ok=True)
os.makedirs(perspective_image_dir, exist_ok=True)

with open(DATA, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    reader_list = list(reader)


for row in reader_list:
    pano_id = row["panorama_id"]
    try:
        pano = streetview.find_panorama_by_id(pano_id)
        panorama_pil_image = streetview.get_panorama(pano=pano)
        panorama_pil_image.save(os.path.join(panorama_dir, f"{pano_id}.jpg"))
        panorama_np_image = np.array(panorama_pil_image)

        max_fov = max(float(row["ocr_width"]), float(row["ocr_height"]))
        fov_scale = 30
        perspective_np_image = e2p(
            panorama_np_image,
            fov_deg=(max_fov * fov_scale, max_fov * fov_scale),
            u_deg=float(row["ocr_yaw"]),
            v_deg=float(row["ocr_pitch"]),
            out_hw=(1024, 1024),
            # in_rot_deg=0,
            mode="bilinear",
        )
        perspective_pil_image = Image.fromarray(perspective_np_image)
        perspective_pil_image.save(
            os.path.join(perspective_image_dir, f"{pano_id}.jpg")
        )

    except Exception as e:
        print(f"Error downloading panorama {pano_id}: {e}")
        raise e
