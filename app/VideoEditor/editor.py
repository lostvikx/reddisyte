import os
import random
from moviepy.editor import *
from moviepy.video import fx


class VideoEditor:
  """
  VideoEditor, used to export a video file.

  Attributes:
    dir_path (str): Real path of this file
    clip (VideoFileClip): Main video track, init with background video
    screenshots (list: ImageClip): A list of image objects
    tts_audio (AudioFileClip) : All TTS audio files concatenated
  """

  def __init__(self, background_video_file=None):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))

    if background_video_file:
      self.clip = VideoFileClip(f"{self.dir_path}/assets/{background_video_file}")


  def set_volume(self, fraction):
    self.clip = self.clip.volumex(fraction)


  def crop_clip(self, width, height):
    # Clip resolution = 1920x1080 & Output resolution = 720x1280
    # print(self.clip.w, self.clip.h) # After resize
    x1 = (self.clip.w - width) / 2
    self.clip = fx.all.crop(self.clip, x1=x1, y1=0, width=width, height=height)


  def cut_clip(self, start_time, clip_duration=60):
    self.clip = self.clip.subclip(start_time, start_time + clip_duration)


  def create_short(self):
    # self.cut_clip(start_time=2)
    # self.set_volume(0.15)

    self.cut_random_clip(clip_duration=60)
    # Find resolution of the video
    clip_res = int(self.clip.h)
    print(f"{clip_res}p video")

    if clip_res == 1080:
      # 1080 * 1.2 ~= 1280
      self.clip = fx.all.resize(self.clip, 1.2)

    self.crop_clip(720, 1280)


  def export(self, file_name):
    final = CompositeVideoClip([self.clip] + self.screenshots).set_audio(self.tts_audio).set_duration(self.tts_audio.duration)
    final.write_videofile(f"{self.dir_path}/../../Videos/{file_name}")


  def add_screenshots(self, path, timestamps):
    self.screenshots = []
    reddit_screenshots = sorted(os.listdir(path), key=lambda name: int(name.split("_")[1].split(".")[0]))

    for i,img in enumerate(reddit_screenshots):
      img_path = f"{path}/{img}"
      ss_img = ImageClip(img_path).set_position(("center", "center")).set_start(timestamps[i]).set_duration(timestamps[i+1]-timestamps[i])
      self.screenshots.append(ss_img)
      try:
        os.remove(img_path)
      except Exception as err:
        print(f"Error: {err}")


  def add_tts(self, path):
    tts_clips = []
    audio_clips = sorted(os.listdir(path), key=lambda name: int(name.split("_")[1].split(".")[0]))
    
    for audio_file in audio_clips:
      audio_file_path = f"{path}/{audio_file}"
      tts_clip = AudioFileClip(audio_file_path)
      tts_clips.append(tts_clip)
      try:
        os.remove(audio_file_path)
      except Exception as err:
        print(f"Error: {err}")

    self.tts_audio = concatenate_audioclips(tts_clips)


  def cut_random_clip(self, clip_duration):
    """
    Cut a random clip of the video of length clip_duration.
    """
    low = clip_duration + (clip_duration // 10)
    high = int(self.clip.duration) - low
    rand_start = random.randrange(low, high)

    # print(rand_start, rand_start + clip_duration)
    self.clip = self.clip.subclip(rand_start, rand_start + clip_duration)

