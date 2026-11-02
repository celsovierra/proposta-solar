import os, sys, threading, webbrowser, traceback


def main():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base)
    gtk = os.path.join(base, "gtk")
    os.environ["WEASYPRINT_DLL_DIRECTORIES"] = gtk
    os.environ["PATH"] = gtk + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory") and os.path.isdir(gtk):
        os.add_dll_directory(gtk)
    import uvicorn
    from app.main import app
    threading.Timer(3, lambda: webbrowser.open("http://localhost:8000")).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)


try:
    main()
except BaseException:
    err = traceback.format_exc()
    pasta = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()
    try:
        with open(os.path.join(pasta, "erro.log"), "w", encoding="utf-8") as f:
            f.write(err)
    except Exception:
        pass
    print(err)
    try:
        input("ERRO! Pressione ENTER para fechar...")
    except Exception:
        pass
