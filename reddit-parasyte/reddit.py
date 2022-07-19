import requests
import random

class Reddit():

  def __init__(self, subreddit, page_sort="top", num_posts=None):
    self.subreddit = subreddit
    self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}.json"
    
    if not num_posts is None:
      self.reddit_url += f"?limit={num_posts}"

    self.req_headers = {"user-agent": "Linux Machine (Vikram Singh Negi)"}

    res = requests.get(self.reddit_url, headers=self.req_headers)
    try:
      res.raise_for_status()
      data = res.json()["data"]
    except Exception as err:
      print(f"Error: {err}")

    self.posts = [child["data"] for child in data["children"]]


  def refine_story_posts(self):
    required_fields = (
      "subreddit", "title", "subreddit_name_prefixed", "upvote_ratio", "ups", "over_18", "spoiler", "id", "is_robot_indexable", "author", "num_comments", "permalink", "url", "subreddit_subscribers", "created_utc", "num_crossposts", "media", "is_video"
    )
    refined_posts = list()

    for post in self.posts:
      new_post = dict()
      for key, val in post.items():
        if (key in required_fields):
          new_post[key] = val
      refined_posts.append(new_post)

    self.posts = refined_posts


  def get_all_posts(self):
    return self.posts.copy()


  def get_random_story_post(self):
    while True:
      rand_post = random.choice(self.posts)
      if rand_post["media"] is None:
        return rand_post
      else:
        continue


  # TODO: extract comments
  def extract_comments(self, post):
    # Sorts the comments by Best
    comments_api_endpoint = f"https://www.reddit.com/r/{self.subreddit}/comments/{post['id']}.json"
    print(comments_api_endpoint)

    res = requests.get(comments_api_endpoint, headers=self.req_headers)
    try:
      res.raise_for_status()

      # Cleaning the data:
      data = [dt["data"] for dt in res.json()[1]["data"]["children"][:-1]]
      print(data[0])
      
    except Exception as err:
      print(f"Error: {err}")

