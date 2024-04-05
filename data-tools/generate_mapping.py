import json
import os

from constants import MIN_ITEM_REVIEWS, MIN_USER_FRIENDS, MIN_USER_REVIEWS, RAW_DIR

if __name__ == "__main__":
    
    data_dir = (
        f"{RAW_DIR}/u_{MIN_USER_REVIEWS}_i_{MIN_ITEM_REVIEWS}_f_{MIN_USER_FRIENDS}"
    )
    out_dir = f"{data_dir}/out"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    
    
    # users
    users_file = f"{data_dir}/users.json"
    with open(f'{users_file}') as f:
        users = [json.loads(line) for line in f]

    users_id = [user['user_id'] for user in users]

    users_map = {
        user_id: user_counter for user_counter, user_id in enumerate(users_id)
    }
    filename= f'{out_dir}/user_map.json'
    with open(filename, 'w') as f:
        json.dump(users_map,f)
        
    print(f"Users map saved to : {filename}")
    
    
    # businesses
    businesses_file = f"{data_dir}/businesses.json"
    with open(businesses_file) as f:
        businesses = [json.loads(line) for line in f]

    businesses_id = [b['business_id'] for b in businesses]

    businesses_map = {
        business_id: c for c, business_id in enumerate(businesses_id)
    }
    filename= f'{out_dir}/item_map.json'
    with open(filename, 'w') as f:
        json.dump(businesses_map,f)
        
    print(f"BUsinesses map saved to : {filename}")
    
    
    