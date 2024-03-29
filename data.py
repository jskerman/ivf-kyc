import praw
import json

from env import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

MAX_COMMENTS = 5

def load_reddit_data(filename: str, kw: str):
    master = []
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/DrumAndBass90).",
        username="DrumAndBass90",
    )

    for submission in reddit.subreddit("IVF").search(kw):
        print("-"*50)
        print(submission.title)
        master.append({
            "title": submission.title,
            "content": submission.selftext,
            "num_comments": submission.num_comments,
            "score": submission.score,
            "top_comments": [comment.body for comment in submission.comments[::MAX_COMMENTS]], 
        })

    with open(f"data/{filename}.json", "w") as f:
        json.dump(master, f)


def read_reddit_data(filename: str):
    with open(f"data/{filename}.json") as f:
        return json.load(f)



