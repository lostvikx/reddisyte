#!/usr/bin/env python3

import requests
import re
from reddit import Reddit

def get_reddit_videos(subreddit="TikTokCringe", page_sort="top", post_limit=10):
  reddit_tiktok_url = f"https://www.reddit.com/r/{subreddit}/{page_sort}.json?limit={post_limit}"
  headers = {"user-agent": "Linux Machine (Vikram Singh Negi)"}

  res = requests.get(reddit_tiktok_url, headers=headers)
  try:
    res.raise_for_status()
    data = res.json()["data"]
  except Exception as err:
    print(f"HTTP Error: {err}")

  # [child["data"] for child in data["children"]][0]

  dt = []
  valid_fields = ["subreddit", "title", "thumbnail", "url_overridden_by_dest",
                  "subreddit_id", "author", "url", "media", "is_video"]

  for child in data["children"]:
    if child["data"]["is_video"]:
      child_data = {}
      for key, val in child["data"].items():
        if key in valid_fields:
          if key == "media":
            fallback_url = val["reddit_video"]["fallback_url"]
            child_data["video_url"] = fallback_url
            child_data["audio_url"] = re.sub(
                r"[\w+\/]DASH_(\d+)", "/DASH_audio", fallback_url)
          else:
            child_data[key] = val
      dt.append(child_data)
  
  return dt, len(dt)


if __name__ == "__main__":
  # print(get_reddit_videos())
  print("who?")
  Reddit().refine_story_post()
