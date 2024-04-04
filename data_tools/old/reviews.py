import json
import os
from pprint import pprint

if __name__ == "__main__":
    
    min_num_user_reviews = 2000
    min_num_user_friends = 20
    min_num_item_reviews = 2000
    BASE_DIR = f'./data/u_{min_num_user_reviews}_i_{min_num_item_reviews}_s_{min_num_user_friends}'
    OUT_DIR = f'{BASE_DIR}/out'
    
    # all users
    all_reviews_filename = f'{BASE_DIR}/all_reviews.txt'
    with open(f'{all_reviews_filename}') as f:
        reviews = [json.loads(line) for line in f]
    
    # load users map
    users_map_file = f'{OUT_DIR}/users_map.json'
    with open(users_map_file, 'r') as f:
        users_map = json.load(f)
        
    # load businesses map
    businesses_map_file = f'{OUT_DIR}/businesses_map.json'
    with open(businesses_map_file, 'r') as f:
        businesses_map = json.load(f)
        
        
    filename = f'{OUT_DIR}/yelp.reviews'
    with open(filename, 'w') as f:
        for review in reviews:
            rating = 1 if review['stars'] >=3 else 0
            f.write(f'{review["review_id"]},{users_map[review["user_id"]]},{businesses_map[review["business_id"]]},{rating}\n')
        
