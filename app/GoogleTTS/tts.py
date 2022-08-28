import os
import ffmpeg
from google.cloud import texttospeech


class GoogleTTS:
  """
  GoogleTTS interacts with the Google text-to-speech API.

  Attributes:
    dir_path (str): real path of this file
    text (list): list of strings to be generated as audio
    audio_timestamps (list: float): timestamps of each audio file
    total_duration (float): total duration of all audio files
  """

  def __init__(self, text:list, lang="en-US", limit_duration=40):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    # Set env variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.dir_path}/creds/service-account-file.json"

    self.text = text
    self.audio_timestamps = [float(0)]
    self.total_duration = float(0)
    clip_count = 0

    print("Saving audio files...")

    for idx, t in enumerate(self.text):
      if self.total_duration >= limit_duration:
        print(f"break: got {clip_count} clips")
        break

      client = texttospeech.TextToSpeechClient()
      synthesis_input = texttospeech.SynthesisInput(text=t)

      voice = texttospeech.VoiceSelectionParams(
        language_code=lang, 
        name=lang+"-Wavenet-G", # G or H
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
      )
      audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
      )
      res = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
      )
      audio_file_name = f"audio_{idx}"
      self.save_audio_file(res_binary=res.audio_content, file_name=audio_file_name)
      clip_count += 1

      # Note: (duration_ts or frames) / sample_rate == duration
      self.total_duration += float(ffmpeg.probe(f"{self.dir_path}/temp/{audio_file_name}.opus")["format"]["duration"])
      self.audio_timestamps.append(round(self.total_duration, 2))

    print(f"Total Duration: {self.total_duration:.2f}")
    self.text = self.text[:clip_count]
    total_char_count = sum([len(t) for t in self.text])
    self.save_char_count(total_char_count)


  def save_audio_file(self, res_binary, file_name):
    audio_file_path = f"{self.dir_path}/temp/{file_name}.opus"

    with open(audio_file_path, "wb") as audio_file:
      audio_file.write(res_binary)


  def save_char_count(self, count):
    with open(f"{self.dir_path}/char_count.txt", "r") as f:
      t_letter_count = int(f.read())
      t_letter_count += count
      
    with open(f"{self.dir_path}/char_count.txt", "w") as f:
      f.write(str(t_letter_count))

    print(f"{1_000_000 - t_letter_count} chars before billing!")


  def get_text_list(self):
    return self.text.copy()


  def get_audio_timestamps(self):
    return self.audio_timestamps.copy()

