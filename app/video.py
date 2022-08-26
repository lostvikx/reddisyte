import os
from reddit import Reddit

def extract_short_video(subreddit, num, page_sort, filter):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  # video: video posts, media with video
  reddit = Reddit(subreddit, content="video", page_sort=page_sort, num_posts=num, filter=filter)
  all_posts = reddit.get_all_posts(no_media=False)
  reddit.display_all_posts_title()

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

  post_title = post_selected["title"].strip()
  print(post_selected)

