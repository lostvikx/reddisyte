#!/usr/bin/env python3

import asyncio
import os
from utils import youtube_video_meta_defaults

from playwright.async_api import async_playwright
from reddit import Reddit
from GoogleTTS.tts import GoogleTTS
from Playwright.screenshot import Playwright
from VideoEditor.editor import VideoEditor
from YTUpload.upload import UploadYT

# TODO: Only titles (no comments) --only-titles
# NOTE: subreddits = ["Showerthoughts", "AskReddit"]


async def run_playwright(url:str, is_nsfw, div_ids:list):
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    play = Playwright(page)
    await play.navigate(url)
    await play.save_screenshots(div_ids, is_nsfw)
    await browser.close()


def main():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  # story: post title + top comments (posts with no media)
  subreddit = "AskReddit"
  reddit = Reddit(subreddit=subreddit, content="story", num_posts=10, filter="day")
  all_posts = reddit.get_all_posts(no_media=True)
  # Display post titles
  reddit.display_all_posts_title()

  # Select a post
  try:
    post_num = int(input("Post Number: "))
    post_selected = all_posts[post_num]
  except:
    print("Enter a valid number!")
    exit()

  post_title = post_selected["title"].strip()
  if post_selected["over_18"]:
    post_title += " [NSFW]"

  # Top 20 comments of a particular post
  comments = reddit.extract_comments(post=post_selected,num_comments=20)

  # Prepare for TTS
  text_list = [post_selected["title"].strip()]

  div_ids_list = [post_selected["name"]]
  for com in comments:
    text_list.append(com["body"].strip())
    div_ids_list.append(com["name"])

  # print(text_list)
  # print(div_ids_list)

  # NOTE: sum(audio_clips) <= 45 seconds
  g_tts = GoogleTTS(text=text_list)
  text_list = g_tts.get_text_list()
  div_ids_list = div_ids_list[:len(text_list)]

  print(g_tts.get_audio_timestamps())

  # Extracting screenshots from the subreddit
  asyncio.run(run_playwright(post_selected["url"], post_selected["over_18"], div_ids_list))

  # Creating the final video
  video = VideoEditor("minecraft_1440p.webm")
  video.create_short()
  video.add_screenshots(path=f"{dir_path}/Playwright/temp", timestamps=g_tts.get_audio_timestamps())
  video.add_tts(path=f"{dir_path}/GoogleTTS/temp")
  vids = len(os.listdir(f"{dir_path}/../Videos"))
  video_file = f"{subreddit.lower()}_{vids}.mp4"
  video.export(video_file)

  # Uploading video to YouTube
  upload = UploadYT()
  vid_meta = {
    "file": f"{dir_path}/../Videos/{video_file}",
    "title": f"{post_title} - r/{subreddit}",
    "description": youtube_video_meta_defaults["descriptions"],
    "keywords": youtube_video_meta_defaults["keywords"],
    "privacy_status": "public"
  }

  youtube = upload.authenticate_service()
  upload.init_upload(youtube,vid_meta)


if __name__ == "__main__":
  main()
