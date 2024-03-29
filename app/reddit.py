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

  def __init__(self, subreddit:str, content:str, page_sort="top", num_posts=None, filter="day"):
    """
    Construct a `Reddit` object, connects to the free reddit API trick.

    Params
      subreddit (str): Target subreddit to fetch data
      content (str): Create a story using threads or compile videos `["story", "video"]`
      page_sort="top" (str): Sort the subreddit posts by one of these `["top", "best", "hot", "new"]`
      num_posts=None (int):Number of posts
      filter=None (str): Filter the posts by `["day", "week", "month", "year"]`
    """
    self.subreddit = subreddit
    print(f"Subreddit: {self.subreddit}")
    self.req_headers = {"user-agent": "Linux Machine (Reddisyte)"}
    self.reddit_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}.json?t={filter}"

    if num_posts: self.reddit_url += f"&limit={num_posts}"
    
    print(self.reddit_url)
    res = requests.get(self.reddit_url, headers=self.req_headers)
    try:
      res.raise_for_status()
      data = res.json().get("data",None)
    except Exception as err:
      print(f"HTTP Error: {err}")
      exit()

    # Post title length < 300 chars
    uncleaned_data = utils.filter_data([child["data"] for child in data["children"]], "title")
    print(f"Posts: {len(uncleaned_data)}")

    if content == "story":
      self.posts = utils.clean_data(uncleaned_data, utils.post_required_fields)
    elif content == "video":
      self.posts = utils.clean_data(uncleaned_data, utils.video_required_fields)


  def get_all_posts(self, no_media) -> list:
    """
    Return all posts.
    """
    if no_media:
      print("Fetching posts with no media...")
      self.posts = [post for post in self.posts if post["media"] is None]
      # Test:
      # for post in self.posts: print({"title": post["title"], "url": post["url"], "media": post["media"]})
    else:
      print("Fetching posts with media (only video)...")
      self.posts = [post for post in self.posts if post.get("media", None) and post.get("video_url", None)]

    return self.posts.copy()


  def display_all_posts_title(self):
    """
    Prints out title of each post.
    """
    count = 0
    for post in self.posts:
      post_title = f"{count}. "
      if post["over_18"]:
        post_title += "[NSFW] "
      if post["spoiler"]:
        post_title += "[SPOILER] "

      post_title += post['title']
      print(post_title)
      count += 1


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
    comments_uri = f"https://www.reddit.com/r/{self.subreddit}/comments/{post['id']}.json"
    print(f"Fetching: {comments_uri}")

    res = requests.get(comments_uri, headers=self.req_headers)
    try:
      res.raise_for_status()

      # Cleaning the data:
      # Comment length < 300 chars
      uncleaned_data = utils.filter_data([dt["data"] for dt in res.json()[1]["data"]["children"][:-1]], "body")
      # TEST: first 20 comments
      comments = utils.clean_data(uncleaned_data, utils.comment_required_fields)[:num_comments]

    except Exception as err:
      print(f"HTTP Error: {err}")

    # comments = [post.pop("replies", None) for post in comments]
    print(f"Comments: {len(comments)}")

    return self.sort_comments(comments)

  # Sort comments by most "ups"
  def sort_comments(self, comments:list)->list:
    return sorted(comments, key=lambda post: post["ups"], reverse=True)

