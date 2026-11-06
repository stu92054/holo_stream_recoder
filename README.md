# holo_stream_recoder
A program that automatically records vtuber live streams

The program is currently in alpha release and may have many unpredictable bugs.

## Getting started
```python3 main.py```

## Server version (`server/`)
The Linux version that ran on the Oracle Cloud `instance-youtubedl` machine (2022-01 ~ 2023-03), recovered on 2026-11-06.

- `dcnotify.py` – Discord bot: posts upcoming Hololive streams (00:00 / 08:00 / 16:00) and auto-records unarchived karaoke streams, `$dl <url>` to download on demand
- `searchlive.py` – Holodex API helpers
- `download.py` / `auto_record.py` – yt-dlp download logic
- `hololive_channels_id.txt` – channels to watch

Secrets are read from environment variables (see `secrets.env.example`):
```
cd server
cp secrets.env.example secrets.env   # fill in DISCORD_TOKEN / HOLODEX_API_KEY
set -a; . ./secrets.env; set +a
python3 dcnotify.py
```
It was originally run inside `screen`; recordings go to `~/downloads/`.
