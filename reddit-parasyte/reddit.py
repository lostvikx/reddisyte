import requests

class Reddit():

  def __init__(self, subreddit="AskReddit", page_sort="top", num_posts=10):
    if num_posts == None:
      self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}.json"
    else:
      self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}.json?limit={num_posts}"

    headers = {"user-agent": "Linux Machine (Vikram Singh Negi)"}

    res = requests.get(self.reddit_url, headers=headers)
    try:
      res.raise_for_status()
      data = res.json()["data"]
    except Exception as err:
      print(f"HTTP Error: {err}")

    self.posts = [child["data"] for child in data["children"]]

    # extract comments
    # example: "https://www.reddit.com/r/{subreddit}/comments/{posts.id}.json"

    # posts_ids =

    # print first post
    print(self.posts[0])

  # def 
