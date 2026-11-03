import os, sys, threading, webbrowser, traceback


def pasta_exe():
    return os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()


def avisar(msg):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, msg, "Proposta Solar", 0x10)
    except Exception:
        pass


def main():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base)
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")
    gtk = os.path.join(base, "gtk")
    os.environ["WEASYPRINT_DLL_DIRECTORIES"] = gtk
    os.environ["PATH"] = gtk + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory") and os.path.isdir(gtk):
        os.add_dll_directory(gtk)
    import uvicorn
    from app.main import app
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_config=None)
    server = uvicorn.Server(config)
    threading.Timer(3, lambda: webbrowser.open("http://localhost:8000")).start()
    try:
        import pystray
        from PIL import Image
        ico = os.path.join(base, "app", "static", "icone.png")
        img = Image.open(ico) if os.path.exists(ico) else Image.new("RGB", (64, 64), (30, 60, 110))

        def sair(icon, item):
            server.should_exit = True
            icon.stop()

        def abrir(icon, item):
            webbrowser.open("http://localhost:8000")

        menu = pystray.Menu(pystray.MenuItem("Abrir Proposta Solar", abrir, default=True),
                            pystray.MenuItem("Sair", sair))
        tray = pystray.Icon("PropostaSolar", img, "Proposta Solar", menu)
        threading.Thread(target=tray.run, daemon=True).start()
    except Exception:
        pass
    server.run()


try:
    main()
except BaseException:
    err = traceback.format_exc()
    try:
        with open(os.path.join(pasta_exe(), "erro.log"), "w", encoding="utf-8") as f:
            f.write(err)
    except Exception:
        pass
    avisar("Erro ao iniciar. Detalhes em erro.log na pasta do programa.\n\n" + err[-400:])
