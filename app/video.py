import os
import subprocess
from utils import select_post
from reddit import Reddit

# NOTE: useful_subreddits = ["TikTokCringe"]


def extract_short_video(subreddit, num, page_sort, filter):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  # video: video posts, media with video
  reddit = Reddit(subreddit, content="video", page_sort=page_sort, num_posts=num, filter=filter)
  all_posts = reddit.get_all_posts(no_media=False)
  reddit.display_all_posts_title()

  # Selecting the perfect video
  while True:
    post_selected = select_post(all_posts)

    # Preview video:
    subprocess.run(["mpv", "--no-terminal", post_selected["video_url"]])
    done = input("Found the perfect one? [Y/n] ").lower()
    if done in ["no", "n"]: continue
    else: break

  # Debug:
  print(post_selected)

  # Save files
  