from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import yt_dlp
import uuid
import os
import socket

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="Universal Media Downloader API"
)

# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# DOWNLOAD FOLDER
# ============================================

BASE_DIR = "/home/Bala/insta-downloader/backend"

DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ============================================
# REQUEST MODEL
# ============================================

class DownloadRequest(BaseModel):
    url: str

# ============================================
# HOME ROUTE
# ============================================

@app.get("/")
def home():

    return {
        "message": "Downloader Backend Running",
        "server": socket.gethostname()
    }

# ============================================
# DOWNLOAD ROUTE
# ============================================

@app.post("/download")
async def download_video(data: DownloadRequest):

    try:

        print("Downloading:", data.url)

        # Unique filename
        unique_id = str(uuid.uuid4())

        output_template = os.path.join(
            DOWNLOAD_DIR,
            f"{unique_id}.%(ext)s"
        )

        # yt-dlp config
        ydl_opts = {

            "cookiefile": "/home/Bala/cookies.txt",

            "outtmpl": output_template,

            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
                ),
                "Referer": "https://www.instagram.com/",
            },

            "quiet": False,
            "verbose": True,
        }

        # Download + extract info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                data.url,
                download=True
            )

            downloaded_file = ydl.prepare_filename(info)

        # Thumbnail handling
        thumbnail = (
            info.get("thumbnail")
            or (
                info.get("thumbnails", [{}])[-1].get("url")
                if info.get("thumbnails")
                else None
            )
        )

        print("Downloaded file:", downloaded_file)

        # Extract actual filename
        actual_filename = os.path.basename(downloaded_file)

        return {

            "success": True,

            "title": info.get(
                "title",
                "Instagram Reel"
            ),

            "thumbnail": thumbnail,

            "download_url": f"/file/{actual_filename}"
        }

    except Exception as e:

        print("DOWNLOAD ERROR:", str(e))

        return {

            "success": False,

            "error": str(e)
        }

# ============================================
# FILE ROUTE
# ============================================

@app.get("/file/{filename}")
async def get_file(filename: str):

    file_path = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    print("Serving file:", file_path)

    if not os.path.exists(file_path):

        return {

            "success": False,

            "message": "File not found"
        }

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )