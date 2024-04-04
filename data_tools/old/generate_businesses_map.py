import json
import os

if __name__ == "__main__":
    
    min_num_user_reviews = 2000
    min_num_user_friends = 20
    min_num_item_reviews = 2000
    BASE_DIR = f'./data/u_{min_num_user_reviews}_i_{min_num_item_reviews}_s_{min_num_user_friends}'
    OUT_DIR = f'{BASE_DIR}/out'
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    # all users
    all_businesses_filename = f'{BASE_DIR}/all_businesses.txt'
    with open(f'{all_businesses_filename}') as f:
        businesses = [json.loads(line) for line in f]

    businesses_id = [b['business_id'] for b in businesses]

    businesses_map = {
        business_id: counter for counter, business_id in enumerate(businesses_id)
    }
    filename= f'{OUT_DIR}/businesses_map.json'
    with open(filename, 'w') as f:
        json.dump(businesses_map,f)
        
    print(f"Businesses map saved to : {filename}")
    
    
    