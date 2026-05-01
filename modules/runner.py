import subprocess

def run_concurrently(files):
    processes = [subprocess.Popen(['python', f]) for f in files]
    for p in processes:
        p.wait()