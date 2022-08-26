import re

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

    if d.get("is_video", None):
      for key, val in d.items():
        if (key in required_fields):
          if key == "media":
            fallback_url = val["reddit_video"]["fallback_url"]
            new_data["video_url"] = fallback_url
            new_data["audio_url"] = re.sub(r"[\w+\/]DASH_(\d+)", "/DASH_audio", fallback_url)
          else:
            new_data[key] = val
    else:
      for key, val in d.items():
        if (key in required_fields):
          new_data[key] = val
    refined_data.append(new_data)

  return refined_data


post_required_fields = ("title", "ups", "over_18", "spoiler", "name", "url", "media", "is_video", "id")
# TODO: Extract only videos
video_required_fields = ("title", "ups", "over_18", "spoiler", "name", "media", "is_video")
# Don't extract replies
comment_required_fields = ("name", "author", "body", "ups")


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
    text = clean_text(d[data_kind])
    d[data_kind] = text

    if len(d[data_kind]) <= length:
      filtered_data.append(d)

  return filtered_data


youtube_video_meta_defaults = {
  "descriptions": "Subscribe for more Reddit content.\nThis video was automatically generated using various APIs.\nBackground video: https://youtu.be/n_Dv4JMiwK8 \nTags: #shorts #reddit #cool",
  "keywords": "reddit,funny,shorts,memes,cool",
}

def print_story(text_list:list):
  for i,t in enumerate(text_list):
    if i == 0: print(t)
    else: print(f"--\n{t}")
