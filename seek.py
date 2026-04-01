import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template

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
