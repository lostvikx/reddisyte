import os
import subprocess

from utils import select_post, save_res_file
from reddit import Reddit
from moviepy.editor import AudioFileClip, AudioClip, VideoFileClip

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

  def render_video(save_dir_path, video_url, audio_url, clip_name):

    n_vids = len(os.listdir(save_dir_path)) - 1

    video_file_ext = video_url.split(".")[-1]
    video_file_name = f"{clip_name}.{video_file_ext}"
    temp_dir = f"{save_dir_path}/temp"

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

      final_clip.write_videofile(f"{save_dir_path}/vid_{n_vids}.mp4")
      os.remove(f"{temp_dir}/{video_file_name}")
      os.remove(f"{temp_dir}/{audio_file_name}")
    else:
      print("No audio file!")
      save_res_file(video_url, f"{save_dir_path}/vid_{n_vids}.mp4")

  render_video(videos_dir_path, video_url, audio_url, clip_name)
