#!/usr/bin/env python3

import asyncio
import os

from playwright.async_api import async_playwright
from reddit import Reddit
from GoogleTTS.tts import GoogleTTS
from Playwright.screenshot import Playwright
from VideoEditor.editor import VideoEditor

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
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=10)
  all_posts = reddit.get_all_posts(no_media=True)
  # Display post titles
  reddit.display_all_posts_title()

  # Select a post
  post_num = int(input("Post Number: "))
  # TODO: Add error handling
  post_selected = all_posts[post_num]

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
  video.export("hello.mp4")


if __name__ == "__main__":
  main()
