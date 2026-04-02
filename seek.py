import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
VIDEO_FOLDER = Path(os.getenv("VIDEO_FOLDER", "."))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/videos")
def videos():
    videos = []

    for file in VIDEO_FOLDER.iterdir():
        videos.append({"title": file.name})

    return videos


@app.route("/play", methods=["POST"])
def play():
    file_name = request.form.get("file", "")
    video_path = VIDEO_FOLDER / file_name

    subprocess.Popen(["mpv", str(video_path.resolve())])
    return "", 202
