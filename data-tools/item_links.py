import json
import os
from pprint import pprint

from matplotlib import category

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS, RAW_DIR

if __name__ == "__main__":
    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    out_dir = f"{data_dir}/out"

    businesses_file = f"{data_dir}/businesses.json"
    item_links_file = f"{out_dir}/item.links"

    # load businesses map
    businesses_map_file = f"{out_dir}/item_map.json"
    with open(businesses_map_file, "r") as f:
        businesses_map = json.load(f)

    with open(businesses_file) as f:
        businesses = [json.loads(line) for line in f]

    businesses = [
        {**b, "categories": [c.strip() for c in b["categories"].split(",")]}
        for b in businesses
    ]

    COMMON_ITEMS_K = 7
    item_links = []
    for i, b1 in enumerate(businesses):
        if len(b1["categories"]) < COMMON_ITEMS_K:
            continue
        for j, b2 in enumerate(businesses):
            if i == j or len(b2["categories"]) < COMMON_ITEMS_K:
                continue
            if (
                len(set(b1["categories"]).intersection(set(b2["categories"])))
                < COMMON_ITEMS_K
            ):
                continue
            item_links.append(
                f"{businesses_map[b1['business_id']]},{businesses_map[b2['business_id']]},0\n"
            )

    with open(item_links_file, "w") as f:
        _ = [f.write(r) for r in item_links]
