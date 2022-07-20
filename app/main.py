#!/usr/bin/env python3

from reddit import Reddit
import random


def main():
  # story: post title + top comments (no media)
  reddit = Reddit(subreddit="AskReddit", content="story", num_posts=20)
  all_posts = reddit.get_all_posts()

  # display post titles
  # count = 0
  # for post in all_posts:
  #   print(f"{count}. {post['title']}")
  #   count += 1

  # rand_story = reddit.get_random_story_post()
  # print(rand_story["title"])
  # comments = reddit.extract_comments(rand_story)
  comments = reddit.extract_comments(all_posts[18])
  print(random.choice(comments)["body"])
  # print(comments[2]["reply"])
  # print([{"ups": post["ups"], "id": post["id"]} for post in comments[:3]])


if __name__ == "__main__":
  main()
