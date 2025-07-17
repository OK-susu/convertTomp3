import os
import sys
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/download")
def download_mp3(url: str = Query(...)):
    # 실행파일 내부일 경우 _MEIPASS 사용
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    # ffmpeg 경로 지정 (Windows용 ffmpeg.exe 포함)
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
