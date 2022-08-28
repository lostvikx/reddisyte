import asyncio
import os
from utils import story_youtube_meta_defaults, print_story, select_post, prompt_final_video_del

from playwright.async_api import async_playwright
from reddit import Reddit
from GoogleTTS.tts import GoogleTTS
from Playwright.screenshot import Playwright
from VideoEditor.editor import VideoEditor
from YTUpload.upload import UploadYT

# TODO: Only titles (no comments) --only-titles
# NOTE: useful_subreddits = ["Showerthoughts", "AskReddit"]


async def run_playwright(url:str, is_nsfw, div_ids:list):
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    play = Playwright(page)
    await play.navigate(url)
    await play.save_screenshots(div_ids, is_nsfw)
    await browser.close()


def create_story(subreddit:str, num:int, filter:str):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  # story: post title + top comments (posts with no media)
  reddit = Reddit(subreddit=subreddit, content="story", num_posts=num, filter=filter)
  all_posts = reddit.get_all_posts(no_media=True)
  # Display post titles
  reddit.display_all_posts_title()
  post_selected = select_post(all_posts)

  post_title = post_selected["title"].strip()
  if post_selected["over_18"]:
    post_title += " [NSFW]"

  # Top 20 comments of a particular post
  comments = reddit.extract_comments(post=post_selected,num_comments=20)

  # Prepare for TTS
  text_list = [post_selected["title"].strip()]

  div_ids_list = [post_selected["name"]]
  for com in comments:
    text_list.append(com["body"])
    div_ids_list.append(com["name"])

  # Print out the title & its comments
  print_story(text_list)
  do = input("Continue? [Y/n] ").lower()
  if do in ["n", "no"]: exit()

  # sum(audio_clips) <= 40 seconds
  g_tts = GoogleTTS(text=text_list, limit_duration=40)
  text_list = g_tts.get_text_list()
  div_ids_list = div_ids_list[:len(text_list)]

  print(g_tts.get_audio_timestamps())

  # Extracting screenshots from the subreddit
  asyncio.run(run_playwright(post_selected["url"], post_selected["over_18"], div_ids_list))

  # Creating the final video
  video = VideoEditor(background_video_file="minecraft_1440p.webm")
  video.create_short()
  video.add_screenshots(path=f"{dir_path}/Playwright/temp", timestamps=g_tts.get_audio_timestamps())
  video.add_tts(path=f"{dir_path}/GoogleTTS/temp")
  vids = len(os.listdir(f"{dir_path}/../Videos"))
  video_file = f"{subreddit.lower()}_{vids}.mp4"
  video.export(video_file)

  # Uploading video to YouTube
  up = input("Upload video on YouTube? [Y/n] ").lower()
  if up in ["n", "no"]: exit()

  upload = UploadYT(channel_name="Reddisyte")

  vid_meta = {
    "file": f"{dir_path}/../Videos/{video_file}",
    "title": f"{post_title} - r/{subreddit}",
    "description": story_youtube_meta_defaults["description"],
    "keywords": story_youtube_meta_defaults["keywords"],
    "privacy_status": "public"
  }

  if len(vid_meta["title"]) >= 100:
    print(f'Title Character Limit!\nTitle: {vid_meta["title"]}')
    new_vid_title = input("Enter a custom YT title: ")
    vid_meta["title"] = f"{new_vid_title} - r/{subreddit}"

  youtube = upload.authenticate_service()
  upload.init_upload(youtube,vid_meta)

  prompt_final_video_del(f"{dir_path}/../Videos/{video_file}")
