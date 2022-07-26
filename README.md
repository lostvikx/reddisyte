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

## TODO

- [ ] Refine comments: remove html tags
- [x] Google TTS API
- [ ] Use playwright package, instead of selenium
- [ ] Create a setup file at root dir

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
