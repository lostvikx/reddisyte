#!/usr/bin/env python3

from reddit import Reddit


def main():
  # story: post title + top comments (no media)
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=10)
  all_posts = reddit.get_all_posts()

  # display post titles
  # for post in all_posts:
  #   print(post["title"])

  rand_story = reddit.get_random_story_post()
  print(rand_story["title"])
  comments = reddit.extract_comments(rand_story)
  print(comments[2]["body"], comments[2]["reply"], sep="\n")


if __name__ == "__main__":
  main()
