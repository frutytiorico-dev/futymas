import hashlib
import os
import re

ARCHIVO = "menu.html"

def hash_archivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def validar_html(path):
    if not os.path.exists(path):
        return "❌ Archivo no existe"

    if os.path.getsize(path) < 100:
        return "⚠️ Archivo demasiado pequeño (posible corrupción)"

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        contenido = f.read()

    if "<html" not in contenido.lower() or "</html>" not in contenido.lower():
        return "❌ HTML incompleto o dañado"

    sospechoso = re.findall(r"(eval\(|document\.write|atob\(|fromCharCode)", contenido, re.I)
    if sospechoso:
        return "⚠️ Posible inserción de código sospechoso"

    return "✅ HTML funcional"

print("Estado:", validar_html(ARCHIVO))
print("Hash SHA256:", hash_archivo(ARCHIVO))
