import re
import requests
import os
import subprocess

from moviepy.editor import AudioFileClip, VideoFileClip


def clean_data(data:iter, required_fields:iter) -> list:
  """
  Returns the list with its dict elements having only the required fields.

  Params:
    data: [ ...dict() ], list of dictionaries
    required_fields: iter()
  
  Returns:
    refined_data: list
  """
  refined_data = []

  for d in data:
    new_data = dict()

    if d.get("is_video", None) or d.get("media", None):

      for key, val in d.items():
        if (key in required_fields):
          if key == "media":
            new_data[key] = True
            fallback_url = val.get("reddit_video",{}).get("fallback_url",None)

            if not fallback_url is None:
              fallback_url = re.sub(r"\?source=fallback","",fallback_url)
              new_data["video_url"] = fallback_url
              new_data["audio_url"] = re.sub(r"DASH_\d+", "DASH_audio", fallback_url)
            else:
              gif_url = val.get("oembed",{}).get("thumbnail_url",None)
              new_data["video_url"] = re.sub(r"\-+mobile\.jpg", ".mp4", gif_url)
              
          else:
            new_data[key] = val

      new_data["is_video"] = True

    elif d.get("preview",None):
      for key, val in d.items():
        if (key in required_fields):
          new_data[key] = val

      new_data["video_url"] = d.get("preview",{}).get("reddit_video_preview",{}).get("fallback_url",None)
      new_data["media"] = True
      new_data["is_video"] = True

    else:
      for key, val in d.items():
        if (key in required_fields):
          new_data[key] = val
    refined_data.append(new_data)

  return refined_data

# Extract story materials
post_required_fields = ("title", "ups", "over_18", "spoiler", "name", "url", "media", "is_video", "id")
comment_required_fields = ("name", "author", "body", "ups") # Don't extract replies
# Extract only videos
video_required_fields = ("title", "ups", "over_18", "spoiler", "name", "media", "is_video", "url")


def clean_text(text:str):
  url_pattern = r"\[?http[s]?:\/{2}\S+\]?"
  clean = re.sub(r"[&#]\w+;","",re.sub(url_pattern,"",text)).strip()

  # Add punctuations:
  punctuations = list(".!?")
  if not clean[-1] in punctuations:
    clean += "."

  return clean


def filter_data(data:list, data_kind, length=300):
  """
  Filter out long data.

  Args:
    data_kind == "title" or "body" (comment)
  """
  filtered_data = []
  for d in data:
    if data_kind == "body":
      text = clean_text(d[data_kind])
      d[data_kind] = text

    if len(d[data_kind]) <= length:
      filtered_data.append(d)

  return filtered_data


story_youtube_meta_defaults = dict(
  description="Subscribe to watch such facinating stories.\nThis video was automatically generated.\nBackground video: https://youtu.be/n_Dv4JMiwK8 \nTags: #shorts #reddit #cool #funny",
  keywords="reddit,funny,shorts,memes,cool",
)

video_youtube_meta_defaults = dict(
  description=(
    "Subscribe to watch such cringy content.\nTags: #shorts #funny #cringe #wholesome",
    "Subscribe for more such awesome content that will blow your mind.\nI don't own any of these videos, make sure to raise any issues regarding my content.\nI'm not proud of producing such content, please don't tell my mom.\nTags: #shorts #bae #babe #cute #outfit #fit #tiktok #lilac #lilacbae #aesthetic #tiktokdance"
  ),
  keywords=(
    "funny,shorts,memes,cringe,cute",
    "shorts,bae,babe,cute,fit,girl,babe,dance,aesthetic,tiktok,tiktokdance"
  )
)

red_meta_defaults = dict(
  description="Subscribe to cure your depression.\nTags: #shorts #cute #outfit #girl #fit",
  keywords="shorts,cute,fit,girl,babe,dance,aesthetic"
)


def print_story(text_list:list):
  for i,t in enumerate(text_list):
    if i == 0: print(t)
    else: print(f"--\n{t}")


def select_post(all_posts:list)->dict:
  # Select a post
  while True:
    try:
      if len(all_posts):
        post_num = int(input("Post Number: "))
        post_selected = all_posts[post_num]
        break
      else:
        raise Exception
    except ValueError:
      print("Enter a valid number!")
      continue
    except:
      print("No posts were found!")
      exit()

  return post_selected


def save_res_file(uri:str, save_path:str):
  with requests.get(uri, stream=True) as res:
    try:
      res.raise_for_status()
      with open(f"{save_path}", "wb") as file:
        for chunk in res.iter_content(chunk_size=None):
          file.write(chunk)
    except Exception as err:
      print(f"HTTP Error: {err}")
      exit()

def render_video(save_dir_path, video_url, audio_url, clip_name):

  n_vids = len(os.listdir(save_dir_path)) - 1

  video_file_ext = video_url.split(".")[-1]
  video_file_name = f"{clip_name}.{video_file_ext}"
  temp_dir = f"{save_dir_path}/temp"

  final_video_file_path = f"{save_dir_path}/vid_{n_vids}.mp4"

  # Save audio file
  if audio_url:
    audio_file_ext = audio_url.split(".")[-1]
    audio_file_name = f"{clip_name}.{audio_file_ext}"

    save_res_file(audio_url, f"{temp_dir}/{audio_file_name}")

    # Change audio file format to .mp3
    if audio_file_ext == "mp4":
      editor = AudioFileClip(f"{temp_dir}/{audio_file_name}")
      audio_file_ext = "mp3"
      audio_file_name = f"{clip_name}.{audio_file_ext}"

      editor.write_audiofile(f"{temp_dir}/{audio_file_name}")
      editor.close()
    
    # Save video file
    save_res_file(video_url, f"{temp_dir}/{video_file_name}")

    video_clip = VideoFileClip(f"{temp_dir}/{video_file_name}")
    audio_clip = AudioFileClip(f"{temp_dir}/{audio_file_name}")
    final_clip = video_clip.set_audio(audio_clip)

    final_clip.write_videofile(final_video_file_path)
    os.remove(f"{temp_dir}/{video_file_name}")
    os.remove(f"{temp_dir}/{audio_file_name}")
  else:
    print("No audio file!")
    save_res_file(video_url, final_video_file_path)

  return final_video_file_path

def prompt_final_video_del(video_path):
  # Delete final video file (Needs checking)
  delete_file = input("Delete final video? [y/N] ").lower()
  if not delete_file in ["y", "yes"]: exit()

  os.remove(video_path)
  print("Final video deleted successfully!")

def clear_terminal():
  subprocess.run(["clear"])