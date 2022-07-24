#!/usr/bin/env python3

from reddit import Reddit
from GoogleTTS.tts import GoogleTTS

# TODO: Only titles (no replies) as option --only-titles

def main():
  # story: post title + top comments (no media)
  # ["Showerthoughts", "AskReddit"]
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=10)
  all_posts = reddit.get_all_posts()

  # Display post titles
  count = 0
  for post in all_posts:
    print(f"{count}. {post['title']}")
    count += 1

  post_num = int(input("Post Number: "))
  post_selected = all_posts[post_num]
  comments = reddit.extract_comments(post=post_selected,num_comments=20)

  text = post_selected["title"] + "\n\n"
  count_comments = 0
  for com in comments:
    # Max text length == 1000
    if len(text) < 1000:
      text += (com["body"].strip() + "\n")
      count_comments += 1
    # print(com["body"])
    # print("---"*5)

  text = text.strip()
  print(text)
  print(f"Total text length: {len(text)} characters")
  print(f"Comments used: {count_comments}")
  # GoogleTTS(text)


if __name__ == "__main__":
  main()
