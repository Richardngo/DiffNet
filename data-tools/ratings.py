import json
import math
import os
import random
from pprint import pprint

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS, RAW_DIR

if __name__ == "__main__":
    
    include_zero_ratings = False
    
    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    out_dir = f"{data_dir}/out"

    reviews_file = f"{data_dir}/reviews.json"

    with open(reviews_file) as f:
        reviews = [json.loads(line) for line in f]

    # load users map
    users_map_file = f"{out_dir}/user_map.json"
    with open(users_map_file, "r") as f:
        users_map = json.load(f)

    # load businesses map
    businesses_map_file = f"{out_dir}/item_map.json"
    with open(businesses_map_file, "r") as f:
        businesses_map = json.load(f)

    # shuffle reviews
    for _ in range(3):
        random.shuffle(reviews)

    total_reviews_count = len(reviews)
    train_size = 0.7
    validation_size = 0.1
    test_size = 0.2

    train_ratings_file = f"{out_dir}/train.ratings"
    validation_ratings_file = f"{out_dir}/validation.ratings"
    test_ratings_file = f"{out_dir}/test.ratings"
    train_ratings_file_graphrec = f"{out_dir}/graphrec.train.ratings"
    test_ratings_file_graphrec = f"{out_dir}/graphrec.test.ratings"

    train_count = math.floor(train_size * total_reviews_count)
    with open(train_ratings_file, "w") as f1, open(train_ratings_file_graphrec, "w") as f2:
        for review in reviews[:train_count]:
            rating = 1 if review["stars"] >= 3 else 0
            if not include_zero_ratings and rating == 0: continue
            f1.write(
                f'{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{rating}\n'
            )
            f2.write(
                f'{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{int(review["stars"])}\n'
            )

    validation_count = math.floor(validation_size * total_reviews_count)
    with open(validation_ratings_file, "w") as f:
        for review in reviews[train_count : train_count + validation_count]:
            rating = 1 if review["stars"] >= 3 else 0
            if not include_zero_ratings and rating == 0: continue
            f.write(
                f'{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{rating}\n'
            )

    with open(test_ratings_file, "w") as f1, open(test_ratings_file_graphrec, "w") as f2:
        for review in reviews[train_count + validation_count :]:
            rating = 1 if review["stars"] >= 3 else 0
            if not include_zero_ratings and rating == 0: continue
            f1.write(
                f'{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{rating}\n'
            )
            f2.write(
                f'{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{int(review["stars"])}\n'
            )
