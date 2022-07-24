import os
from google.cloud import texttospeech


class GoogleTTS():

  def __init__(self, text:str, lang="en-US"):
    # Get realpath of this file
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.dir_path}/creds/service-account-file.json"

    self.text = text
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=self.text)

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

    self.res = res
    self.save_audio_file()
    self.save_char_count()


  def save_audio_file(self):
    audio_file_path = f"{self.dir_path}/tts_audio/output.opus"
    with open(audio_file_path, "wb") as audio_file:
      audio_file.write(self.res.audio_content)
      print(f"Audio file saved {audio_file_path}")


  def save_char_count(self):
    with open(f"{self.dir_path}/char_count.txt", "r") as f:
      t_letter_count = int(f.read())

    for c in self.text:
      t_letter_count += 1

    print(f"{1_000_000 - t_letter_count} characters left for TTS API before billing!")
    with open(f"{self.dir_path}/char_count.txt", "w") as f:
      f.write(str(t_letter_count))

