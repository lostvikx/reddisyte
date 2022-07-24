# Reddit Parasyte
Basically steal content from Reddit and post it as shorts on YouTube and earn free money 💰

## Useful Links
- [Top Subreddits](https://www.remote.tools/remote-work/best-subreddits)
- [GDocs Library](https://cloud.google.com/text-to-speech/docs/create-audio-text-client-libraries)

## TODO

- [ ] Refine comments: remove html tags, links | add a fullstop at the end if no mark
- [ ] Hook up Google TTS API
- [ ] Use playwright package, instead of selenium
- [ ] Create a setup file at root dir

# App Directory Tree

```bash
./app/
├── GoogleTTS
│   ├── char_count.txt
│   ├── creds
│   │   └── service-account-file.json
│   ├── tts_audio
│   │   └── output.opus
│   └── tts.py
├── main.py
├── reddit.py
├── story.py
└── utils.py
```
