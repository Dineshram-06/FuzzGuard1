import subprocess
import time

# Launch test app
test_proc = subprocess.Popen(['python', 'test_app.py'])

# Wait a bit
time.sleep(2)

# Launch fuzzer backend
fuzzer_proc = subprocess.Popen(['python', '../app.py'])

print("Demo running: Test app on http://127.0.0.1:5001, Fuzzer API on http://127.0.0.1:5000")
print("Run frontend separately with npm run dev")

# Wait for Ctrl+C
try:
    fuzzer_proc.wait()
except KeyboardInterrupt:
    test_proc.terminate()
    fuzzer_proc.terminate()