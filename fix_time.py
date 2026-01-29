import os
import time
from datetime import datetime

FILE = "menu.html"

now = time.time()

# Modifica acceso y modificación
os.utime(FILE, (now, now))

print("✔ Access y Modify actualizados:", datetime.now())

# ⚠ CrearTime requiere Windows API
try:
    import ctypes
    from ctypes import wintypes

    FILE_WRITE_ATTRIBUTES = 0x100
    OPEN_EXISTING = 3

    handle = ctypes.windll.kernel32.CreateFileW(
        FILE,
        FILE_WRITE_ATTRIBUTES,
        0,
        None,
        OPEN_EXISTING,
        0,
        None
    )

    if handle != -1:
        wintime = int((now + 11644473600) * 10000000)
        ft = wintypes.FILETIME(wintime & 0xFFFFFFFF, wintime >> 32)

        ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(ft), None, None)
        ctypes.windll.kernel32.CloseHandle(handle)

        print("✔ CreationTime actualizado")
except Exception as e:
    print("⚠ No se pudo cambiar CreationTime:", e)
