import os
import subprocess
from utils import select_post
from reddit import Reddit

def extract_short_video(subreddit, num, page_sort, filter):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  # video: video posts, media with video
  reddit = Reddit(subreddit, content="video", page_sort=page_sort, num_posts=num, filter=filter)
  all_posts = reddit.get_all_posts(no_media=False)
  reddit.display_all_posts_title()
  post_selected = select_post(all_posts)
  post_title = post_selected["title"].strip()

  print(post_selected)

  # Preview video:
  subprocess.run(["mpv", "--no-terminal", post_selected["video_url"]])

