from data import read_reddit_data, load_reddit_data
from extract import extract_model
import json
import pandas

KEYWORD = input("keyword\n> ")

load_reddit_data(kw=KEYWORD)
data = read_reddit_data(KEYWORD)
master = []

for i, post in enumerate(data):
    try:
        print(f"Extracting {i + 1} of {len(data)}")
        extracted_result = extract_model.invoke(
            {
                "post": f"{post['title']}\n{post['content']}", 
                "comments": "\n".join(post['top_comments'])
            }
        )
        extracted_result["link"] = post["link"]
        extracted_result["score"] = post["score"]
        master.append(extracted_result)
    except Exception as e:
        print(f"Something went wrong, moving on... {str(e)}")

with open(f"data/{KEYWORD}-processed.json", "w") as f:
    json.dump(master, f)

df = pandas.DataFrame(master)
df.to_csv(f"data/{KEYWORD}-processed.csv", index=False)
