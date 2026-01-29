import os
import hashlib
import time
import subprocess
import psutil
from datetime import datetime

# ========= CONFIG =========
HTML_FILE = "menu.html"
EXE_FILE = ""
BASELINE_DIR = "baseline"
CPU_THRESHOLD = 80        # %
MEMORY_THRESHOLD = 500    # MB
CHECK_TIME = 10           # segundos
# ==========================

os.makedirs(BASELINE_DIR, exist_ok=True)

# ---------- UTILIDADES ----------
def sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def save_baseline(name, value):
    with open(os.path.join(BASELINE_DIR, name), "w") as f:
        f.write(value)

def load_baseline(name):
    path = os.path.join(BASELINE_DIR, name)
    return open(path).read() if os.path.exists(path) else None

# ---------- VALIDAR HTML ----------
def validate_html(path):
    print("\n[HTML] Validando:", path)

    if not os.path.exists(path):
        print("❌ HTML no existe")
        return

    size = os.path.getsize(path)
    hash_now = sha256(path)
    hash_old = load_baseline("html.hash")

    print("✔ Tamaño:", size, "bytes")
    print("✔ Hash:", hash_now)

    if hash_old:
        if hash_now != hash_old:
            print("⚠ CAMBIO DETECTADO → posible inserción de código")
        else:
            print("✔ Sin cambios detectados")
    else:
        save_baseline("html.hash", hash_now)
        print("ℹ Baseline HTML creado")

    # análisis simple de código
    with open(path, encoding="utf-8", errors="ignore") as f:
        code = f.read()

    suspicious = ["eval(", "while(true)", "setInterval(", "document.write", "innerHTML"]
    found = [s for s in suspicious if s in code]

    if found:
        print("⚠ Código potencialmente peligroso:", found)
    else:
        print("✔ Código HTML/JS limpio")

# ---------- VALIDAR EXE ----------
def validate_exe(path):
    print("\n[EXE] Validando:", path)

    if not os.path.exists(path):
        print("❌ EXE no existe")
        return

    size = os.path.getsize(path)
    hash_now = sha256(path)
    hash_old = load_baseline("exe.hash")

    print("✔ Tamaño:", size, "bytes")
    print("✔ Hash:", hash_now)

    if hash_old:
        if hash_now != hash_old:
            print("⚠ CAMBIO EN EXE → posible corrupción o modificación")
        else:
            print("✔ EXE sin cambios")
    else:
        save_baseline("exe.hash", hash_now)
        print("ℹ Baseline EXE creado")

# ---------- ANALIZAR EJECUCIÓN ----------
def analyze_execution(path):
    print("\n[MEMORIA / EJECUCIÓN] Analizando:", path)

    try:
        proc = subprocess.Popen(path)
        time.sleep(2)

        p = psutil.Process(proc.pid)
        start = time.time()

        while time.time() - start < CHECK_TIME:
            cpu = p.cpu_percent(interval=1)
            mem = p.memory_info().rss / 1024 / 1024

            print(f"CPU: {cpu:.1f}% | MEM: {mem:.1f} MB")

            if cpu > CPU_THRESHOLD:
                print("⚠ Posible bucle infinito (CPU alta)")
                break

            if mem > MEMORY_THRESHOLD:
                print("⚠ Uso de memoria anormal")
                break

        proc.terminate()
        print("✔ Proceso cerrado correctamente")

    except Exception as e:
        print("❌ Error ejecutando EXE:", e)

# ---------- MAIN ----------
if __name__ == "__main__":
    print("\n=== VALIDADOR DE ARCHIVOS ===")
    print("Fecha:", datetime.now())

    validate_html(HTML_FILE)
    validate_exe(EXE_FILE)

    if os.path.exists(EXE_FILE):
        analyze_execution(EXE_FILE)

    print("\n=== VALIDACIÓN FINALIZADA ===")
