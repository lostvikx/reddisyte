import os
import subprocess

from utils import select_post, render_video, video_youtube_meta_defaults, prompt_final_video_del, clear_terminal
from reddit import Reddit
from YTUpload.upload import UploadYT

# NOTE: useful_subreddits = ["TikTokCringe"]


def extract_short_video(subreddit, num, page_sort, filter):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  videos_dir_path = f"{dir_path}/../Videos"
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

  # Save files:
  video_url = post_selected.get("video_url")  # Cannot be None, must be a str
  audio_url = post_selected.get("audio_url", None)
  clip_name = post_selected.get("name", "test")

  video_path = render_video(videos_dir_path, video_url, audio_url, clip_name)

  # Uploading video on YouTube
  up = input("Upload video on YouTube? [Y/n] ").lower()
  if up in ["n", "no"]: exit()

  clear_terminal()

  # Select a channel to upload:
  channels = ["YawningMocha", "LilacBae"]
  for i, name in enumerate(channels): print(i, name)

  while True:
    try:
      select_channel = int(input(f"Select a YouTube Channel: "))
      channel_name = channels[select_channel]
      break
    except:
      print("Please select a valid channel")
      continue

  upload = UploadYT(channel_name=channel_name)

  vid_title = post_selected.get('title')
  print(f"Sample Title: {vid_title}")
  t = input("Wanna use this as the title? [Y/n] ").lower()
  if t in ["no", "n"]: vid_title = input("Enter YT video title: ")

  vid_meta = dict(
    file=video_path,
    title=vid_title,
    description=video_youtube_meta_defaults.get("description")[select_channel],
    keywords=video_youtube_meta_defaults.get("keywords")[select_channel],
    privacy_status="public"
  )

  youtube = upload.authenticate_service()
  upload.init_upload(youtube,vid_meta)

  prompt_final_video_del(video_path)
