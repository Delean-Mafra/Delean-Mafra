import speedtest
import subprocess

def run_speedtest():
    result = subprocess.run(['speedtest-cli'], capture_output=True, text=True)
    return result.stdout

output = run_speedtest()
print(output)