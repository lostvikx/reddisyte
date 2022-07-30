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
    for key, val in d.items():
      if (key in required_fields):
        new_data[key] = val
    refined_data.append(new_data)

  return refined_data

post_required_fields = ("title", "ups", "over_18", "spoiler", "name", "url", "media", "is_video", "id")
# TODO: Extract only videos
video_required_fields = ()
# Don't extract replies
comment_required_fields = ("name", "author", "body", "ups")

def filter_data(data:list, data_kind, length=300):
  """
  Filter out long data.
  """
  # data_kind := title or comment
  filtered_data = []
  for d in data:
    if len(d[data_kind]) <= length:
      filtered_data.append(d)

  return filtered_data

def clean_text(text):
  pass

youtube_video_meta_defaults = {
  "descriptions": "Subscribe for more Reddit content.\nThis video was automatically generated using various APIs.\nBackground video: https://youtu.be/n_Dv4JMiwK8 \nTags: #shorts #reddit #cool",
  "keywords": "reddit,funny,shorts,memes,cool",
}

# print(youtube_video_meta_defaults["descriptions"])
