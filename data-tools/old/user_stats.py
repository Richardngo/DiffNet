import json
import os
from collections import defaultdict
from pprint import pprint

if __name__ == "__main__":
    
    
    MINIFY_REVIEWS_FILE_PATH = '/Users/dharahastallapally/Downloads/archive/yelp_academic_dataset_review_minify.json'
    # all users
    with open(MINIFY_REVIEWS_FILE_PATH) as f:
        reviews = [json.loads(line) for line in f]


    changes = True
    counter = 1
    while changes:
        user_reviews = defaultdict(list)
        business_reviews = defaultdict(list)
        for review in reviews:
            user_reviews[review['user_id']].append(review['text'])
            business_reviews[review['business_id']].append(review['text'])
        user_stats = {
            u_id: len(val) for u_id, val in user_reviews.items()
        }
        business_stats = {
            b_id: len(val) for b_id, val in business_reviews.items()
        }
        # pprint(user_stats)

        users_reviews_gt_k = {k:v for k,v in user_stats.items() if v>=2}
        business_reviews_gt_k = {k:v for k,v in business_stats.items() if v>=2}
        pprint(f"\n======================================\nCurrent counter: {counter}")
        pprint(f'orignal_users: {len(user_stats)} and updated users: {len(users_reviews_gt_k)}')
        pprint(f'orignal_businesses: {len(business_stats)} and updated businesses: {len(business_reviews_gt_k)}')
        changes = len(user_stats) != len(users_reviews_gt_k) or len(
            business_stats
        ) != len(business_reviews_gt_k)
        counter +=counter
        reviews = [
            r
            for r in reviews
            if r['user_id'] in users_reviews_gt_k
            and r['business_id'] in business_reviews_gt_k
        ]

    OUT_DIR = './data/reviews,json'
    with open(OUT_DIR, 'w') as f:
        _=[f.write(f'{json.dumps(r)}\n') for r in reviews]
    
    print("Data process complete")
    