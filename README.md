# Reddit Parasyte
Basically steal content from Reddit and post it as shorts on YouTube and earn free money 💰

## Usage
```bash
sudo apt install ffmpeg
pip install -r requirements.txt
playwright install
```

## Useful Links

- [Top Subreddits](https://www.remote.tools/remote-work/best-subreddits)
- [GDocs Library](https://cloud.google.com/text-to-speech/docs/create-audio-text-client-libraries)
- [Background Video](https://www.youtube.com/watch?v=n_Dv4JMiwK8&ab_channel=bbswitzer)
- [YouTube Docs](https://developers.google.com/youtube/v3/guides/uploading_a_video)

## TODO

- [x] Google TTS API
- [x] Use playwright package to extract screenshots
- [ ] Refine comments: remove html tags
- [ ] Give credit to background video in description
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
├── reddit.py
├── story.py
└── utils.py
```
