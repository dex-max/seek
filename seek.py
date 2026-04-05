import os
import subprocess
from pathlib import Path
from urllib.parse import unquote

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory

load_dotenv()

app = Flask(__name__)

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm"}
VIDEO_FOLDER = Path(os.getenv("VIDEO_FOLDER", "."))
THUMBNAIL_FOLDER = Path("thumbnails")
THUMBNAIL_FOLDER.mkdir(parents=True, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/videos")
def videos():
    videos = []

    for file in VIDEO_FOLDER.iterdir():
        if file.suffix.lower() in VIDEO_EXTENSIONS:
            videos.append({"title": file.name})

    return videos


@app.route("/thumbnail/<video_filename>")
def thumbnail(video_filename):
    video_path = VIDEO_FOLDER / unquote(video_filename)
    thumbnail_filename = get_thumbnail(video_path)

    return send_from_directory(THUMBNAIL_FOLDER, thumbnail_filename)


@app.route("/play", methods=["POST"])
def play():
    file_name = request.form.get("file", "")
    video_path = VIDEO_FOLDER / file_name

    subprocess.Popen(["mpv", str(video_path.resolve())])
    return "", 202


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()

    download_cmd = [
        "yt-dlp",
        "--write-info-json",
        "-o",
        str(VIDEO_FOLDER / "%(title)s.%(ext)s"),
        url,
    ]

    subprocess.Popen(download_cmd)
    return "", 202


def get_thumbnail(video_path):
    filename = f"{video_path.stem}.jpg"
    thumbnail_path = THUMBNAIL_FOLDER / filename

    if thumbnail_path.exists():
        return filename

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-dump_attachment:t:0",
            str(thumbnail_path),
            "-i",
            str(video_path),
        ]
    )

    if thumbnail_path.exists():
        return filename

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "00:00:05",
            "-i",
            str(video_path),
            "-vframes",
            "1",
            "-vf",
            "scale=480:-1",
            str(thumbnail_path),
        ]
    )

    if thumbnail_path.exists():
        return filename

    return ""
