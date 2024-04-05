import json

from constants import *

with open(REVIEWS_FILE_PATH, "r") as fread, open(
    MINIFY_REVIEWS_FILE_PATH, "w"
) as fwrite:
    for line in fread:
        review = json.loads(line)
        review_min = {
            "review_id": review["review_id"],
            "user_id": review["user_id"],
            "business_id": review["business_id"],
            "stars": review["stars"],
            "text": review["text"],
        }
        fwrite.write(f"{json.dumps(review_min)}\n")

print("All reviews are processed")


with open(USERS_FILE_PATH, "r") as f_read, open(MINIFY_USERS_FILE_PATH, "w") as f_write:
    for line in f_read:
        user = json.loads(line)
        user_min = {
            "user_id": user["user_id"],
            "friends": [f.strip() for f in user["friends"].split(",")],
        }
        f_write.write(f"{json.dumps(user_min)}\n")
print("All users are processed")


with open(BUSINESS_FILE_PATH, "r") as f_read, open(
    MINIFY_BUSINESS_FILE_PATH, "w"
) as f_write:
    for line in f_read:
        business = json.loads(line)
        user_min = {
            "business_id": business["business_id"],
            "categories": business["categories"],
        }
        f_write.write(f"{json.dumps(user_min)}\n")

print("All businesses are processed")

print("task complete")