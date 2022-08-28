import httplib2
import os
import json
import argparse

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

parser = argparse.ArgumentParser()
parser.add_argument("--auth_host_name", default="localhost")
parser.add_argument("--noauth_local_webserver", default=False)
parser.add_argument("--logging_level")
parser.add_argument("--auth_host_port", default=[8080,8090])

class UploadYT:
  """
  Uploads video to YouTube using the YouTube Data v3 API.

  Attributes:
    dir_path (str): Real path of this file
  """

  def __init__(self, channel_name):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    self.channel_name = channel_name


  def authenticate_service(self):
    flow = flow_from_clientsecrets(
      filename=f"{self.dir_path}/creds/client_secret.json",
      scope="https://www.googleapis.com/auth/youtube.upload"
    )

    oauth_file_path = f"{self.dir_path}/creds/{self.channel_name}_oauth2.json"

    storage = Storage(oauth_file_path)
    creds = storage.get()
    flags = parser.parse_args("--auth_host_name localhost --logging_level INFO".split())

    # Browser pop-up window to authenticate account
    try:
      with open(oauth_file_path, "r") as f:
        oauth_token = json.load(f)

        if oauth_token["invalid"]:
          print("Credentials expired!")
          creds = run_flow(flow, storage, flags)
          
    except FileNotFoundError:
      print("OAuth2 file not found!")
      creds = run_flow(flow, storage, flags)

    return build("youtube", "v3", http=creds.authorize(httplib2.Http()))


  def init_upload(self, youtube, options):
    tags = None
    if options["keywords"]:
      tags = [t.strip() for t in options["keywords"].split(",")]

    body = {
      "snippet": {
        "title": options["title"],
        "description": options["description"],
        "tags": tags,
      },
      "status": {
        "privacyStatus": options["privacy_status"]
      }
    }

    insert_vid = youtube.videos().insert(
      part=",".join(body.keys()),
      body=body,
      media_body=MediaFileUpload(options["file"], chunksize=-1, resumable=True)
    )

    self.resumable_upload(insert_vid)


  def resumable_upload(self, insert_req):
    res = None
    while res is None:
      try:
        print("Uploading video...")
        status, res = insert_req.next_chunk()
        if res is not None:
          print(f"Video: https://www.youtube.com/shorts/{res['id']} was uploaded!")
      except Exception as err:
        print(f"Error: {err}")
        exit()
