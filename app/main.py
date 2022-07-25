#!/usr/bin/env python3

from reddit import Reddit
from GoogleTTS.tts import GoogleTTS

# TODO: Only titles (no comments) --only-titles
# NOTE: subreddits = ["Showerthoughts", "AskReddit"]

# def prepare_text_for_tts(*text):
#   print(for )


def main():
  # story: post title + top comments (posts with no media)
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=10)
  all_posts = reddit.get_all_posts(no_media=True)
  # Display post titles
  reddit.display_all_posts_title()

  # Select a post
  post_num = int(input("Post Number: "))
  post_selected = all_posts[post_num]

  # Top 20 comments of a particular post
  comments = reddit.extract_comments(post=post_selected,num_comments=20)

  # Prepare for TTS
  text = [post_selected["title"].strip()] + [com["body"].strip() for com in comments]

  # text = post_selected["title"] + "\n\n"
  # count_comments = 0
  # for com in comments:
  #   # Max text length == 1000
  #   if len(text) < 1000:
  #     text += (com["body"].strip() + "\n")
  #     count_comments += 1

  # text = text.strip()
  # print(text)
  # print(f"Total text length: {len(text)} characters")
  # print(f"Comments used: {count_comments}")
  # GoogleTTS(text)


if __name__ == "__main__":
  main()
