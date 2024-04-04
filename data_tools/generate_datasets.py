import json
import os
from collections import defaultdict
from pprint import pprint

from constants import (
    MIN_ITEM_REVIEWS,
    MIN_USER_FRIENDS,
    MIN_USER_REVIEWS,
    MINIFY_BUSINESS_FILE_PATH,
    MINIFY_REVIEWS_FILE_PATH,
    MINIFY_USERS_FILE_PATH,
    RAW_DIR,
)

if __name__ == "__main__":

    with open(MINIFY_REVIEWS_FILE_PATH, "r") as f:
        reviews = [json.loads(line) for line in f]
    # discard reviews less thant 3
    reviews = [r for r in reviews if r['stars']>=3]

    users = defaultdict()
    with open(MINIFY_USERS_FILE_PATH, "r") as f:
        for line in f:
            u = json.loads(line)
            users[u["user_id"]] = u

    with open(MINIFY_BUSINESS_FILE_PATH, "r") as f:
        businesses = defaultdict()
        for line in f:
            b = json.loads(line)
            businesses[b["business_id"]] = b

    isDiff = True
    counter = 1

    while isDiff:
        user_reviews = defaultdict(list)
        business_reviews = defaultdict(list)
        for r in reviews:
            user_reviews[r["user_id"]].append(r["text"])
            business_reviews[r["business_id"]].append(r["text"])

        user_stats = {u_id: len(val) for u_id, val in user_reviews.items()}
        business_stats = {b_id: len(val) for b_id, val in business_reviews.items()}
        user_friends_stats = {u_id: len(u["friends"]) for u_id, u in users.items()}

        conditional_user_reviews = {
            k: v for k, v in user_stats.items() if v >= MIN_USER_REVIEWS 
        }
        conditional_business_reviews = {
            k: v for k, v in business_stats.items() if v >= MIN_ITEM_REVIEWS
        }
        conditional_user_friends = {
            k: v for k, v in user_friends_stats.items() if v >= MIN_USER_FRIENDS
        }

        pprint(f"\n======================================\nCurrent counter: {counter}")
        pprint(
            f"original_users: {len(user_stats)} and updated users: {len(conditional_user_reviews)}"
        )
        pprint(
            f"original_businesses: {len(business_stats)} and updated businesses: {len(conditional_business_reviews)}"
        )

        # update users, values, reviews
        users = {
            k: v
            for k, v in users.items()
            if k in conditional_user_reviews and k in conditional_user_friends
        }
        for u in users.values():
            friends = [
                f
                for f in u["friends"]
                if f in conditional_user_reviews and f in conditional_user_friends
            ]
            u["friends"] = friends

        businesses = {
            k: v for k, v in businesses.items() if k in conditional_business_reviews
        }

        reviews = [
            r
            for r in reviews
            if r["user_id"] in users and r["business_id"] in businesses
        ]

        isDiff = (
            len(user_stats) != len(conditional_user_reviews)
            or len(business_stats) != len(conditional_business_reviews)
            or len(user_friends_stats) != len(conditional_user_friends)
        )

        counter += 1

    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    reviews_file = f"{data_dir}/reviews.json"
    users_file = f"{data_dir}/users.json"
    business_file = f"{data_dir}/businesses.json"

    with open(reviews_file, "w") as f:
        _ = [f.write(f"{json.dumps(r)}\n") for r in reviews]

    with open(users_file, "w") as f:
        _ = [f.write(f"{json.dumps(u)}\n") for u in users.values()]

    with open(business_file, "w") as f:
        _ = [f.write(f"{json.dumps(b)}\n") for b in businesses.values()]

    print("Data process complete")
