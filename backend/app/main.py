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

DOWNLOAD_DIR = "downloads"

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
        filename = f"{uuid.uuid4()}.mp4"

        output_path = os.path.join(
            DOWNLOAD_DIR,
            filename
        )

        # yt-dlp config
        ydl_opts = {

            "format": "best",

            "outtmpl": output_path,

            "merge_output_format": "mp4",

            "noplaylist": True,

            "quiet": False,

            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(iPhone; CPU iPhone OS 15_0 like Mac OS X)"
                )
            }
        }

        # Download + extract info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                data.url,
                download=True
            )

        # Thumbnail handling
        thumbnail = (
            info.get("thumbnail")
            or (
                info.get("thumbnails", [{}])[-1].get("url")
                if info.get("thumbnails")
                else None
            )
        )

        print("Download completed")

        return {

            "success": True,

            "title": info.get(
                "title",
                "Instagram Reel"
            ),

            "thumbnail": thumbnail,

            "download_url": f"/file/{filename}"
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