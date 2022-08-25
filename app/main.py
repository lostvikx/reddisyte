#!/usr/bin/env python3

import story
from argparse import ArgumentParser


def main():
  parser = ArgumentParser(description="A simple terminal tool to scrape Reddit for content, because good artists borrow, great artists steal.")
  group = parser.add_mutually_exclusive_group(required=True)

  # Can ignore this:
  group.add_argument("-s","--create-story",action="store_true",help="create a video story using reddit comments and use text-to-speech for narration, then upload with minecraft background video")
  group.add_argument("-v","--short-video",action="store_true",help="simply download & upload a short video, preferably less than 60s")
  group.add_argument("-c","--compilation-video",action="store_true",help="download a bunch of short videos & compile them together, then upload")

  args = parser.parse_args()

  if args.create_story: story.create_story()
  elif args.short_video: print("short video fn")
  elif args.compilation_video: print("compile fn")  


if __name__ == "__main__":
  main()
