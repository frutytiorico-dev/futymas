import subprocess
import time
import os
import datetime
import csv

BROWSER = r"C:\Program Files\Mozilla Firefox\firefox.exe"
HTML = r"C:\Users\YENY\Desktop\fast\Kil.html"
OUTDIR = "exec_trace"
INTERVAL = 2  # segundos

os.makedirs(OUTDIR, exist_ok=True)

def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    ).stdout

ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logfile = f"{OUTDIR}\\stream_{ts}.log"

print("[*] Launching Kil.html...")
firefox_proc = subprocess.Popen([BROWSER, HTML])
root_pid = firefox_proc.pid

print(f"[+] Firefox root PID: {root_pid}")

tracked_pids = set()
alive_pids = {}

with open(logfile, "w", encoding="utf-8") as log:
    log.write(f"STREAM START {ts}\n")
    log.write(f"ROOT_FIREFOX_PID={root_pid}\n\n")

print("[*] Streaming PID monitoring started (CTRL+C to stop)\n")

try:
    while True:
        snapshot = run(
            "powershell -Command "
            "\"Get-CimInstance Win32_Process | "
            "Select-Object ProcessId,ParentProcessId,Name,CommandLine | "
            "ConvertTo-Csv -NoTypeInformation\""
        )

        reader = csv.DictReader(snapshot.splitlines())
        current = {}

        for row in reader:
            pid = int(row["ProcessId"])
            ppid = int(row["ParentProcessId"])
            name = row["Name"]
            cmd = row["CommandLine"] or ""

            # 🔗 Asociación REAL
            if (
                pid == root_pid or
                ppid == root_pid or
                "firefox.exe" in name.lower()
            ):
                current[pid] = (ppid, name, cmd)

        # ➕ nuevos
        for pid in current:
            if pid not in tracked_pids:
                tracked_pids.add(pid)
                alive_pids[pid] = time.time()

                msg = f"[+] PID CREATED {pid} PPID={current[pid][0]} NAME={current[pid][1]}"
                print(msg)

                with open(logfile, "a", encoding="utf-8") as log:
                    log.write(msg + "\n")
                    log.write(f"CMD: {current[pid][2]}\n\n")

        # ➖ muertos
        for pid in list(tracked_pids):
            if pid not in current:
                tracked_pids.remove(pid)

                msg = f"[-] PID TERMINATED {pid}"
                print(msg)

                with open(logfile, "a", encoding="utf-8") as log:
                    log.write(msg + "\n")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n[!] Monitoring stopped by user")

    with open(logfile, "a", encoding="utf-8") as log:
        log.write("\nSTREAM TERMINATED BY USER\n")

print("\n[✓] Streaming execution trace completed.")
