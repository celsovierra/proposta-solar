import os, sys, threading, webbrowser
base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
os.chdir(base)
os.environ["WEASYPRINT_DLL_DIRECTORIES"] = os.path.join(base, "gtk")
import uvicorn
from app.main import app
threading.Timer(3, lambda: webbrowser.open("http://localhost:8000")).start()
uvicorn.run(app, host="127.0.0.1", port=8000)
