import json
import os
from pprint import pprint

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS, RAW_DIR

if __name__ == "__main__":
    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    out_dir = f"{data_dir}/out"

    users_file = f"{data_dir}/users.json"
    social_links_file = f"{out_dir}/user.links"

    # users
    with open(users_file) as f:
        users = [json.loads(line) for line in f]

    users_id = [user["user_id"] for user in users]

    # load users map
    users_map_file = f"{out_dir}/user_map.json"
    with open(users_map_file, "r") as f:
        users_map = json.load(f)
    # pprint(users_map)

    with open(social_links_file, "w") as fl:
        for user in users:
            friends = user["friends"]
            friends = [f for f in friends if f in users_id]

            _ = [
                fl.write(f'{users_map[user["user_id"]]},{users_map[f]}, 0\n')
                for f in friends
            ]
