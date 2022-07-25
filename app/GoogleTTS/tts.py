import os
from google.cloud import texttospeech

# NOTE: Not asynchronous

class GoogleTTS():

  def __init__(self, text:list, lang="en-US"):
    # Get realpath of this file
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    # Set env variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.dir_path}/creds/service-account-file.json"

    self.text = text
    self.total_char_count = sum([len(t) for t in self.text])

    print("Saving audio files...")
    for idx, t in enumerate(self.text):
      client = texttospeech.TextToSpeechClient()
      synthesis_input = texttospeech.SynthesisInput(text=t)

      voice = texttospeech.VoiceSelectionParams(
        language_code=lang, 
        name=lang+"-Wavenet-H",
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

      self.save_audio_file(res_binary=res.audio_content, file_name=f"audio_{idx}")

    print("Audio files saved")
    self.save_char_count()


  def save_audio_file(self, res_binary, file_name):
    audio_file_path = f"{self.dir_path}/temp/{file_name}.opus"

    with open(audio_file_path, "wb") as audio_file:
      audio_file.write(res_binary)


  def save_char_count(self):
    with open(f"{self.dir_path}/char_count.txt", "r") as f:
      t_letter_count = int(f.read())
      t_letter_count += self.total_char_count
      
    with open(f"{self.dir_path}/char_count.txt", "w") as f:
      f.write(str(t_letter_count))

    print(f"{1_000_000 - t_letter_count} chars before billing!")

