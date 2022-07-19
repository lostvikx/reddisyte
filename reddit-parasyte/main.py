#!/usr/bin/env python3

from reddit import Reddit


def main():
  # Story: Post title + Top comments (no media)
  reddit = Reddit(subreddit="AskReddit", num_posts=10)
  reddit.refine_story_posts()
  all_posts = reddit.get_all_posts()

  # Test: display post titles
  # for post in all_posts:
  #   print(post["title"])

  rand_story = reddit.get_random_story_post()
  # print(rand_story)
  reddit.extract_comments(rand_story)


if __name__ == "__main__":
  main()
