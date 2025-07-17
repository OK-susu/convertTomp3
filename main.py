import os
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/download")
def download_mp3(url: str = Query(...)):
    os.makedirs("downloads", exist_ok=True)

    ffmpeg_path = "/usr/bin/ffmpeg"  # Render에서 apt로 설치한 위치

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'keepvideo': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        return FileResponse(path=filename, filename=os.path.basename(filename), media_type='audio/mpeg')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render가 주는 포트 환경변수 사용
    uvicorn.run(app, host="0.0.0.0", port=port)
