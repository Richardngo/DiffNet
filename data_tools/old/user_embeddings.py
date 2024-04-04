import json
import os
from collections import defaultdict
from pprint import pprint

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS

if __name__ == "__main__":
    

    BASE_DIR = f'./data/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_s_{MIN_USER_FRIENDS}'
    OUT_DIR = f'{BASE_DIR}/out'
    
    # all users
    all_reviews_filename = f'{BASE_DIR}/all_reviews.txt'
    with open(f'{all_reviews_filename}') as f:
        reviews = [json.loads(line) for line in f]
        
    user_reviews = defaultdict(list)
    for review in reviews:
        user_reviews[review['user_id']].append(review['text'])
    user_stats = {
        u_id: len(val) for u_id, val in user_reviews.items()
    }
    # pprint(user_stats)
    
    users_reviews_gt_k = {k:v for k,v in user_stats.items() if v>=2}
    pprint(f'orignal_users: {len(user_stats)} and updated users: {len(users_reviews_gt_k)}')
    