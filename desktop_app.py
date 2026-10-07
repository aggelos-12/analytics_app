import subprocess
import time
import database
import webview

streamlit_procces = subprocess.Popen(
    ["streamlit", "run", "streamlit_app.py", "--server.headless=true", "--server.port=8501"]
    )

time.sleep(4)

window = webview.create_window(
    "My app",
    "http://localhost:8501",
    width=1600,
    height=800,
    
)

webview.start()


streamlit_procces.terminate()