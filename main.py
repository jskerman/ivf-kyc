from data import read_reddit_data, load_reddit_data
from extract import extract_model
import json
import pandas

KEYWORD = "finance"

load_reddit_data("reddit", kw=KEYWORD)
data = read_reddit_data("reddit")
master = []

for i, post in enumerate(data):
    print(f"Extracting {i + 1} of {len(data)}")
    extracted_result = extract_model.invoke({"post": f"{post['title']}\n{post['content']}", "comments": "\n".join(post['top_comments'])})
    master.append(extracted_result)

with open("data/processed.json", "w") as f:
    json.dump(master, f)

df = pandas.DataFrame(master)
df.to_csv("data/processed.csv", index=False)
