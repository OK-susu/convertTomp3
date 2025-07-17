import os
import sys
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/download")
def download_mp3(url: str = Query(...)):

    if getattr(sys, 'frozen', False):
        # 빌드된 .exe 실행 중일 때: 현재 실행파일 기준 경로
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    ffmpeg_path = os.path.join(base_path, "bin", "ffmpeg.exe")
    # 다운로드 폴더 생성
    os.makedirs("downloads", exist_ok=True)

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
        return FileResponse(
            path=filename,
            filename=os.path.basename(filename),
            media_type='audio/mpeg'
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
