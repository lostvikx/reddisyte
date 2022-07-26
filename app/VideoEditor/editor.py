import os
import random
from moviepy.editor import *

class VideoEditor():
  def __init__(self):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))


  def add_background_video(self, video_file_name):
    self.clip = VideoFileClip(f"{self.dir_path}/assets/{video_file_name}.mp4")


  def set_volume(self, fraction):
    self.clip = self.clip.volumex(fraction)


  def cut_random_short_clip(self, clip_duration=50):
    low = clip_duration + (clip_duration // 10)
    high = int(self.clip.duration) - low
    rand_start = random.randrange(low, high)

    print(rand_start, rand_start + clip_duration)
    self.clip = self.clip.subclip(rand_start, rand_start + clip_duration)


  def save_short(self, save_file_name):
    self.clip.write_videofile(f"{self.dir_path}/assets/out/{save_file_name}.mp4")


video = VideoEditor()
video.add_background_video("raw_minecraft")
video.cut_random_short_clip()
video.set_volume(0.15)
video.save_short("minecraft_bg")
