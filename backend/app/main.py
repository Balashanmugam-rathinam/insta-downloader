from fastapi import FastAPI, BackgroundTasks
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
    allow_origins=[
        "https://insta-downloader-lemon.vercel.app"
    ],
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

        url = data.url.lower()

        # ============================================
        # BLOCK YOUTUBE
        # ============================================

        if "youtube.com" in url or "youtu.be" in url:

            return {

                "success": False,

                "error": "YouTube downloads are currently not supported"
            }

        # ============================================
        # SUPPORTED PLATFORMS
        # ============================================

        supported_sites = [
            "instagram.com",
            "tiktok.com",
            "facebook.com",
            "x.com",
            "twitter.com"
        ]

        if not any(site in url for site in supported_sites):

            return {

                "success": False,

                "error": "Please paste a valid supported URL"
            }

        # ============================================
        # UNIQUE FILE
        # ============================================

        unique_id = str(uuid.uuid4())

        output_template = os.path.join(
            DOWNLOAD_DIR,
            f"{unique_id}.%(ext)s"
        )

        # ============================================
        # YT-DLP OPTIONS
        # ============================================

        ydl_opts = {

            "outtmpl": output_template,

            "quiet": False,
            "verbose": True,
        }

        # ============================================
        # INSTAGRAM CONFIG
        # ============================================

        if "instagram.com" in url:

            ydl_opts["cookiefile"] = "/home/Bala/cookies.txt"

            ydl_opts["http_headers"] = {

                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
                ),

                "Referer": "https://www.instagram.com/",
            }

        # ============================================
        # DOWNLOAD
        # ============================================

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                data.url,
                download=True
            )

            downloaded_file = ydl.prepare_filename(info)

        # ============================================
        # THUMBNAIL
        # ============================================

        thumbnail = (
            info.get("thumbnail")
            or (
                info.get("thumbnails", [{}])[-1].get("url")
                if info.get("thumbnails")
                else None
            )
        )

        actual_filename = os.path.basename(downloaded_file)

        print("Downloaded:", actual_filename)

        return {

            "success": True,

            "title": info.get(
                "title",
                "Downloaded Media"
            ),

            "thumbnail": thumbnail,

            "download_url": f"/file/{actual_filename}"
        }

    # ============================================
    # HANDLE DOWNLOAD ERRORS
    # ============================================

    except yt_dlp.utils.DownloadError as e:

        print("YT-DLP ERROR:", str(e))

        return {

            "success": False,

            "error": "Failed to download media"
        }

    # ============================================
    # HANDLE OTHER ERRORS
    # ============================================

    except Exception as e:

        print("SERVER ERROR:", str(e))

        return {

            "success": False,

            "error": "Internal server error"
        }

# ============================================
# FILE ROUTE
# ============================================

@app.get("/file/{filename}")
async def get_file(
    filename: str,
    background_tasks: BackgroundTasks
):

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

    # ============================================
    # AUTO DELETE FILE AFTER DOWNLOAD
    # ============================================

    background_tasks.add_task(
        os.remove,
        file_path
    )

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename,
        background=background_tasks
    )