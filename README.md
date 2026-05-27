# Universal Media Downloader

A full-stack media downloader built using FastAPI, Vercel, Azure Ubuntu VM, yt-dlp, and DuckDNS.

Supports downloading media from:

- Instagram
- TikTok
- Facebook
- Twitter/X

---

# Live Demo

Frontend:
https://insta-downloader-lemon.vercel.app

Backend:
https://instadownloaderapi.duckdns.org/docs

---

# Features

- FastAPI backend
- Vercel frontend
- Azure Ubuntu VM hosting
- yt-dlp integration
- Instagram cookie authentication
- Auto file cleanup
- Cron-based storage cleanup
- Secure CORS configuration
- URL validation
- Production deployment using systemd
- HTTPS support using DuckDNS

---

# Tech Stack

## Frontend

- Next.js
- React
- Tailwind CSS
- Vercel

## Backend

- FastAPI
- Python
- yt-dlp
- Uvicorn

## Cloud & DevOps

- Azure Ubuntu VM
- systemd
- DuckDNS
- Linux Cron Jobs

---

# Project Structure

```bash
insta-downloader/
│
├── backend/
│   ├── app/
│   │   └── main.py
│   │
│   ├── downloads/
│   ├── venv/
│   └── requirements.txt
│
├── frontend/
│
└── README.md
```

---

# Backend Setup

## Clone Repository

```bash
git clone <your-repo-url>
cd insta-downloader/backend
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Backend Locally

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

# Production Deployment (Azure VM)

## Create systemd Service

```bash
sudo nano /etc/systemd/system/insta-backend.service
```

Example:

```ini
[Unit]
Description=Instagram Downloader Backend
After=network.target

[Service]
User=Bala
WorkingDirectory=/home/Bala/insta-downloader/backend
ExecStart=/home/Bala/insta-downloader/backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable insta-backend
sudo systemctl start insta-backend
```

---

## Check Status

```bash
sudo systemctl status insta-backend
```

---

# Instagram Cookies Setup

Export Instagram cookies using:

https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

Save cookies file:

```bash
/home/Bala/cookies.txt
```

---

# Auto Cleanup

Files are automatically deleted:

- after serving download
- by cron cleanup every 30 minutes

## Cron Cleanup

```bash
crontab -e
```

Add:

```bash
*/30 * * * * find /home/Bala/insta-downloader/backend/downloads -type f -mmin +30 -delete
```

---

# Useful Commands

## Restart Backend

```bash
sudo systemctl restart insta-backend
```

## View Logs

```bash
journalctl -u insta-backend -f
```

## Check Storage

```bash
df -h
```

## Check Downloads Folder Size

```bash
du -sh /home/Bala/insta-downloader/backend/downloads
```

---

# Security Notes

Add `.gitignore`

```gitignore
venv/
downloads/
cookies.txt
__pycache__/
```

Never upload cookies to GitHub.

---

# Future Improvements

- Docker deployment
- Redis queue system
- Celery workers
- Nginx reverse proxy
- Cloudflare integration
- Rate limiting
- User authentication
- Analytics dashboard

---

# Author

Balashanmugam R

---

# License

MIT License
