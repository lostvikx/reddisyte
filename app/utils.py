def clean_data(data:iter, required_fields:iter) -> list:
  """
  Returns the list with its dict elements having only the required fields.

  Params:
    data: [ ...dict() ], list of dictionaries
    required_fields: iter()
  
  Returns:
    refined_data: list
  """
  refined_data = list()

  for d in data:
      new_data = dict()
      for key, val in d.items():
        if (key in required_fields):
          new_data[key] = val
      refined_data.append(new_data)

  return refined_data

story_required_fields = (
  "subreddit", "title", "upvote_ratio", "ups", "over_18", "spoiler", "id", "is_robot_indexable", "author", "num_comments", "url", "created_utc", "media", "is_video"
)

comment_required_fields = (
  "subreddit", "replies", "id", "author", "body", "ups"
)

def filter_data(data:iter, data_kind, length=100):
  """
  Filter out long data.
  """
  # data_kind := title or comment
  filtered_data = []
  for d in data:
    if len(d[data_kind]) <= length:
      filtered_data.append(d)

  return filtered_data