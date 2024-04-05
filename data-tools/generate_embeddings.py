import json

import numpy as np

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS, RAW_DIR

if __name__ == "__main__":

    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    out_dir = f"{data_dir}/out"

    user_embeddings = np.load(f"{data_dir}/user_embeddings.npy", allow_pickle=True)

    # load users map
    users_map_file = f"{out_dir}/user_map.json"
    with open(users_map_file, "r") as f:
        users_map = json.load(f)

    sort_user_embeddings = [user_embeddings.item().get(user) for user in users_map]
    np.save(f"{out_dir}/user.embeddings.npy", sort_user_embeddings)

    # item embeddings
    business_embeddings = np.load(f"{data_dir}/item_embeddings.npy", allow_pickle=True)
    # load businesses map

    businesses_map_file = f"{out_dir}/item_map.json"
    with open(businesses_map_file, "r") as f:
        businesses_map = json.load(f)

    sort_business_embeddings = [
        business_embeddings.item().get(b) for b in businesses_map
    ]
    np.save(f"{out_dir}/item.embeddings.npy", sort_business_embeddings)
