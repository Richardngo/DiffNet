import json
import os

from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.database import Database

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS


def fetch_and_save_users_by_reviews_and_friend(db: Database, reviews_count: int, friends_count: int, filename: str)->list:
    
    coll= db['user']
    users = list(coll.find({"$and": [{"review_count": {"$gt": reviews_count}}, {"friends_count": {"$gt": friends_count}}]},{"user_id": 1, "friends": 1, "_id": 0}))
    with open(filename, 'w') as f:
        _ = [f.write(f'{json.dumps(user)}\n') for user in users]
    return users

def fetch_and_save_businesses_by_review_count(db: Database, reviews_count: int, filename: str)->list:
    coll = db['business']
    businesses  = list(coll.find({"review_count": {"$gt": reviews_count}},{"business_id": 1,"categories":1, "_id": 0}))
    with open(filename, 'w') as f:
        _ = [f.write(f'{json.dumps(business)}\n') for business in businesses]
    return businesses

def fetch_and_save_review_by_users_and_businesses(db: Database, users: list[str], businesses: list[str], filename: str) -> list:
    coll = db['review']
    reviews =list(coll.find({"$and": [{"user_id":{"$in": users}}, {"business_id":{"$in": businesses}}]} , {"_id": 0, "review_id":1, "user_id": 1, "business_id":1, "stars": 1, "text": 1}))
    with open(filename, 'w') as f:
        _ = [f.write(f'{json.dumps(review)}\n') for review in reviews]
    return reviews

def fetch_and_save_user_reviews(db: Database, user_id: str, businesses: list[str], filename: str)->None:
    coll = db['review']
    user_reviews = list(coll.find({"$and": [{"user_id": user_id}, {"business_id": {"$in": businesses}}]}, {"_id": 0, "review_id":1, "user_id": 1, "business_id":1, "stars": 1, "text": 1}))
    with open(filename, 'w') as f:
        _ = [f.write(f'{json.dumps(review)}\n') for review in user_reviews]
        
def fetch_and_save_business_reviews(db: Database, business_id: str, users: list[str], filename: str)->None:
    coll = db['review']
    business_reviews = list(coll.find({"$and": [{"business_id": business_id}, {"user_id": {"$in": users}}]}, {"_id": 0, "review_id":1, "user_id": 1, "business_id":1, "stars": 1, "text": 1}))
    with open(filename, 'w') as f:
        _ = [f.write(f'{json.dumps(review)}\n') for review in business_reviews]

def generate_datasets(data_dir: str, user_review_count: int, user_friends_count:int, item_reviews_count:int, force_retry: bool = False) -> None:
    
    client: MongoClient = MongoClient()
    db = client['yelp']
    
    # all users
    all_users_filename = f'{data_dir}/all_users.txt'
    if force_retry or not os.path.exists(all_users_filename):
        users = fetch_and_save_users_by_reviews_and_friend(db, user_review_count, user_friends_count, all_users_filename)
        print(f"Users with review_counts > {user_review_count} and friends_count > {user_friends_count} are saved to file: {all_users_filename}\n")
    else:
        with open(f'{all_users_filename}') as f:
            users = [json.loads(line) for line in f]
    
    # all business
    all_businesses_filename = f'{data_dir}/all_businesses.txt'
    if force_retry or not os.path.exists(all_businesses_filename):
        businesses = fetch_and_save_businesses_by_review_count(db, item_reviews_count, all_businesses_filename)
        print(f"Businesses with review_counts > {user_review_count} are saved to file: {all_businesses_filename}\n")
    else:
        with open(f'{all_businesses_filename}') as f:
            businesses = [json.loads(line) for line in f]
    
    # all reviews
    all_reviews_filename = f'{data_dir}/all_reviews.txt'
    if force_retry or not os.path.exists(all_reviews_filename):    
        # extract ids from users and businesses
        users_id = [user['user_id'] for user in users]
        businesses_id = [business['business_id'] for business in businesses]
        reviews = fetch_and_save_review_by_users_and_businesses(db, users_id, businesses_id, all_reviews_filename)
        print(f"Reviews saved to file: {all_reviews_filename}")
    else:
        with open(f'{all_reviews_filename}') as f:
            reviews = [json.loads(line) for line in f]
    
    # users_id = [user['user_id'] for user in users]
    # businesses_id = [business['business_id'] for business in businesses]
    
    # # user reviews
    # all_user_reviews_dir = f'{data_dir}/user_reivews'
    # if not os.path.isdir(all_user_reviews_dir):
    #     os.makedirs(all_user_reviews_dir)
    
    # for user_id in users_id:
    #     fetch_and_save_user_reviews(db, user_id, businesses_id, f'{all_user_reviews_dir}/{user_id}.txt')
    
    # # user reviews
    # all_business_reviews_dir = f'{data_dir}/business_reivews'
    # if not os.path.isdir(all_business_reviews_dir):
    #     os.makedirs(all_business_reviews_dir)
    # for business_id in businesses_id:
    #     fetch_and_save_business_reviews(db, business_id, users_id, f'{all_user_reviews_dir}/{business_id}.txt')
    
    print(f"users: {len(users)} and businesses: {len(businesses)}")
    client.close()
    

if __name__ == "__main__":
    
    
    
    BASE_DIR = f'./data/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_s_{MIN_USER_FRIENDS}'
    if not os.path.isdir(BASE_DIR):
        os.makedirs(BASE_DIR)
    generate_datasets(BASE_DIR, MIN_USER_REVIEWS, MIN_USER_FRIENDS, MIN_ITEM_REVIEWS, force_retry=True)
    