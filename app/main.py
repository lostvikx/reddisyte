#!/usr/bin/env python3

import story
import video
# import compilation

from argparse import ArgumentParser


def main():
  parser = ArgumentParser(description="A simple terminal tool to scrape Reddit for content, because good artists borrow, great artists steal.")
  group = parser.add_mutually_exclusive_group(required=True)

  # Main commands:
  group.add_argument("-s","--story",action="store_true",help="create a video story using reddit comments and use text-to-speech for narration, then upload with minecraft background video")
  group.add_argument("-v","--video",action="store_true",help="simply download & upload a short video, preferably less than 60s")
  group.add_argument("-c","--compilation",action="store_true",help="download a bunch of short videos & compile them together, then upload")

  # Optionals:
  parser.add_argument("--subreddit",help="provide subreddit to extract content from",type=str)
  parser.add_argument("--num-posts",help="number of posts to extract from the subreddit",default=10,type=int)
  parser.add_argument("--filter-time",choices=["hour","day","week","month","quarter","year","all"],help="filter posts by a time period",default="day")
  parser.add_argument("--page-sort",choices=["hot","new","top","rising"],help="sort page in by different trending status",default="top")

  args = parser.parse_args()
  print(args)

  # Call different program according to the input
  if args.story: 
    story.create_story(subreddit=(args.subreddit or "AskReddit"), num=args.num_posts, filter=args.filter_time)
  elif args.video: 
    video.extract_short_video(subreddit=(args.subreddit or "TikTokCringe"), num=args.num_posts, page_sort=args.page_sort,filter=args.filter_time)
  elif args.compilation: 
    print("compile fn")


if __name__ == "__main__":
  main()
