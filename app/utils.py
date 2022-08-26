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

    if d.get("is_video", None) or d.get("media", None):
      is_gif_video = False

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
              is_gif_video = True
              
          else:
            if is_gif_video: new_data["is_video"] = True
            else: new_data[key] = val
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
