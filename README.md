# Reddit Parasyte
Basically steal content from Reddit and post it as shorts on YouTube and earn free money 💰

## Usage
```bash
sudo apt install ffmpeg
cd reddisyte/ && pip install -r requirements.txt
playwright install
```

## Useful Links

- [Top Subreddits](https://www.remote.tools/remote-work/best-subreddits)
- [GDocs Library](https://cloud.google.com/text-to-speech/docs/create-audio-text-client-libraries)
- [Background Video](https://youtu.be/n_Dv4JMiwK8)
- [YouTube Docs](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [YouTube Data API Quota](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas?project=reddisyte)

## TODO

- [x] Google TTS API
- [x] Use playwright package to extract screenshots
- [ ] Clean comments, before initializing TTS
- [x] Give credit to background video in description
- [ ] Create a setup file at root directory

## App Directory Tree

```bash
app/
├── GoogleTTS
│   ├── char_count.txt
│   ├── creds
│   │   └── service-account-file.json
│   ├── temp
│   └── tts.py
├── main.py
├── Playwright
│   ├── screenshot.py
│   └── temp
├── reddit.py
├── rough_work.py
├── utils.py
├── VideoEditor
│   ├── assets
│   │   └── minecraft_1440p.webm
│   ├── editor.py
└── YTUpload
    ├── creds
    │   ├── client_secret.json
    │   └── oauth2.json
    └── upload.py
```
