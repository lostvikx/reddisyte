import httplib2
import os

from googleapiclient.discovery import build
# from apiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

class UploadYT():
  """
  Uploads video to YouTube using the YouTube Data v3 API.

  Attributes:
    dir_path (str): Real path of this file
  """

  def __init__(self):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    
  def authenticate_service(self):
    flow = flow_from_clientsecrets(
      filename=f"{self.dir_path}/creds/client_secret.json",
      scope="https://www.googleapis.com/auth/youtube.upload"
    )

    storage = Storage(f"{self.dir_path}/creds/oauth2.json")
    creds = storage.get()

    if creds is None or creds.invalid:
      creds = run_flow(flow, storage)

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

