import requests
import random
import utils

class Reddit():
  """
  Reddit object, interacts with the free reddit API.

  Attributes:
    subreddit (str): The subreddit to target
    reddit_url (str): API endpoint trick that returns a JSON object
    req_headers (dict): Defines the HTTP request headers necessary for making the request to the API
    posts (list): A list of post objects, includes the metadata of each post
  """

  def __init__(self, subreddit: str, content: str, page_sort="top", num_posts=None):
    """
    Construct a `Reddit` object, connects to the free reddit API trick.

    Params
      subreddit (str): Target subreddit to fetch data
      content (str): Create a story using threads or compile videos `["story", "video"]`
      page_sort="top" (str): Sort the subreddit posts by one of these `["top", "best", "hot", "new"]`
      num_posts=None (int):Number of posts
    """
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
      print(f"HTTP Error: {err}")

    uncleaned_data = [child["data"] for child in data["children"]]

    if content == "story":
      self.posts = utils.clean_data(uncleaned_data, utils.story_required_fields)
    else:
      self.posts = uncleaned_data


  def get_all_posts(self) -> list:
    """
    Return all posts.
    """
    return self.posts.copy()


  def get_random_story_post(self) -> dict:
    """
    Return a random post object.
    """
    while True:
      rand_post = random.choice(self.posts)
      if rand_post["media"] is None:
        return rand_post
      else:
        continue


  def extract_comments(self, post: dict, num_comments=20) -> list:
    """
    Extract top comments of a post (each comment is dict). Can have a reply to that comment.

    Params:
      post (dict): A post object
      num_comments (int): Number of comments
    
    Returns:
      Returns a list of comments.
    """
    # Sorts the comments by Best
    comments_api_endpoint = f"https://www.reddit.com/r/{self.subreddit}/comments/{post['id']}.json"
    print(comments_api_endpoint)

    res = requests.get(comments_api_endpoint, headers=self.req_headers)
    try:
      res.raise_for_status()

      # Cleaning the data:
      uncleaned_data = [dt["data"] for dt in res.json()[1]["data"]["children"][:-1]]
      # TEST: first 20 comments
      comments = utils.clean_data(uncleaned_data, utils.comment_required_fields)[:num_comments]

      for post in comments:
        try:
          post["reply"] = post["replies"]["data"]["children"][0]["data"]["body"]
        except Exception as err:
          # No reply
          post["reply"] = "NA"

        del post["replies"]

      # print(data)
    except Exception as err:
      print(f"HTTP Error: {err}")

    return comments

