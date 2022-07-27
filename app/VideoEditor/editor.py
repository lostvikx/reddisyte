import os
import random
from moviepy.editor import *
from moviepy.video import fx

test_timestamps = [0, 3.342875, 12.818999999999999, 25.897167]

class VideoEditor():
  def __init__(self):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))


  def load_video(self, video_file_name):
    self.clip = VideoFileClip(f"{self.dir_path}/assets/{video_file_name}.mp4")


  def set_volume(self, fraction):
    self.clip = self.clip.volumex(fraction)


  def cut_random_short_clip(self, clip_duration=50):
    """
    Cut a random clip of the video of length clip_duration.
    """
    low = clip_duration + (clip_duration // 10)
    high = int(self.clip.duration) - low
    rand_start = random.randrange(low, high)

    print(rand_start, rand_start + clip_duration)
    self.clip = self.clip.subclip(rand_start, rand_start + clip_duration)


  def crop_clip(self, width, height):
    # Clip resolution = 1920x1080 & Output resolution = 720x1280
    print(self.clip.w, self.clip.h)

    x1 = (self.clip.w - width) / 2
    self.clip = fx.all.crop(self.clip, x1=x1, y1=0, width=width, height=height)


  def cut_clip(self, start_time=5, clip_duration=50):
    self.clip = self.clip.subclip(start_time, start_time+clip_duration)


  def save_short(self, save_file_name):
    self.clip = self.clip.subclip(10,20)
    # self.cut_clip() # Remove the line above
    self.set_volume(0.15)
    self.clip = fx.all.resize(self.clip, 1.2)
    self.crop_clip(720, 1280)
    self.clip.write_videofile(f"{self.dir_path}/assets/out/{save_file_name}.mp4")


video = VideoEditor()
video.load_video("chill_video")
# video.cut_random_short_clip(clip_duration=50)
video.save_short("chill_bg")

