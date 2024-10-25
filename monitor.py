import os
import time
import subprocess

def is_script_running(script_name):
    try:
        # Check if the script is running
        result = subprocess.check_output(f'tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq {script_name}"', shell=True)
        return script_name in result.decode()
    except subprocess.CalledProcessError:
        return False

def restart_script(script_name):
    # Restart the script
    subprocess.Popen(['python', script_name])

script_name = r'ZN-Hospital-WSIs-Rename.py'

while True:
    if not is_script_running(script_name):
        print(f"{script_name} is not running. Restarting...")
        time.sleep(5)
        restart_script(script_name)
    else:
        print(f"{script_name} is running.")
    time.sleep(5)