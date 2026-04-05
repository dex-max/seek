import os
import queue
import subprocess
import threading
from pathlib import Path
from urllib.parse import unquote

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    render_template,
    request,
    send_from_directory,
)

load_dotenv()

app = Flask(__name__)

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm"}
VIDEO_FOLDER = Path(os.getenv("VIDEO_FOLDER", "."))
THUMBNAIL_FOLDER = Path("thumbnails")
THUMBNAIL_FOLDER.mkdir(parents=True, exist_ok=True)
event_queues = []
event_queues_lock = threading.Lock()


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


@app.route("/videos/events")
def video_events():
    def event_stream():
        event_queue = queue.Queue()
        with event_queues_lock:
            event_queues.append(event_queue)

        try:
            while True:
                event = event_queue.get()
                yield f"data: {event}\n\n"
        finally:
            with event_queues_lock:
                event_queues.remove(event_queue)

    return Response(event_stream(), mimetype="text/event-stream")


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

    threading.Thread(target=download_and_update, args=(url,), daemon=True).start()
    return "", 202


def download_and_update(url):
    download_cmd = [
        "yt-dlp",
        "--write-info-json",
        "-o",
        str(VIDEO_FOLDER / "%(title)s.%(ext)s"),
        url,
    ]

    subprocess.run(download_cmd)
    with event_queues_lock:
        for queue in event_queues:
            queue.put("refresh")


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
