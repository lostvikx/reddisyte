import requests

class Reddit():

  def __init__(self, subreddit="AskReddit", page_sort="top", num_posts=10):
    if num_posts == None:
      self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}/.json"
    else:
      self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}/.json?limit={num_posts}"

    headers = {"user-agent": "Linux Machine (Vikram Singh Negi)"}

    res = requests.get(self.reddit_url, headers=headers)
    try:
      res.raise_for_status()
      data = res.json()["data"]
    except Exception as err:
      print(f"HTTP Error: {err}")

    self.posts = [child["data"] for child in data["children"]]


  def refine_story_post(self):
    required_fields = ("subreddit", "title", "subreddit_name_prefixed", "upvote_ratio", "ups", "over_18", "spoiler", "id", "is_robot_indexable", "author", "num_comments", "permalink", "url", "subreddit_subscribers", "created_utc", "num_crossposts", "media", "is_video")
    refined_posts = list()

    for post in self.posts:
      new_post = dict()
      for key, val in post.items():
        if (key in required_fields):
          new_post[key] = val
      refined_posts.append(new_post)

    self.posts = refined_posts

    # Test: display post titles
    for post in self.posts:
      print(post["title"])

  def get_posts(self):
    return self.posts.copy()

  # TODO: extract comments
  # example: "https://www.reddit.com/r/{subreddit}/comments/{posts.id}/.json"
  # posts_ids

