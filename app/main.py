#!/usr/bin/env python3

import random

from reddit import Reddit


def main():
  # story: post title + top comments (no media)
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=10)
  all_posts = reddit.get_all_posts()

  # display post titles
  count = 0
  for post in all_posts:
    print(f"{count}. {post['title']}")
    count += 1

  post_num = int(input("Post Number: "))
  comments = reddit.extract_comments(all_posts[post_num])
  # print(random.choice(comments)["body"])

  for com in comments:
    print(com["body"])
    print("---"*5)


if __name__ == "__main__":
  main()
