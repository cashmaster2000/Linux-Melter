import winreg as reg
import os
import shutil
import sys
import time

def install_persistence():
    # Get the path of the current script (on the USB)
    current_path = os.path.abspath(__file__)
    
    # Define the destination in AppData (hidden folder)
    appdata_dir = os.environ['APPDATA']
    dest_dir = os.path.join(appdata_dir, "SystemMonitor")
    dest_script = os.path.join(dest_dir, "kill_stick_daemon.py")
    
    # Create directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Copy the daemon script to the hidden location
    # Assuming you save the code below as 'kill_stick_daemon.py'
    # In a real scenario, you'd embed the source or copy it dynamically
    if not os.path.exists(dest_script):
        # If running from USB, we might need to copy the file there first
        # For this example, we assume the file is already in the same dir
        try:
            shutil.copy(__file__, dest_script)
        except Exception as e:
            print(f"Error copying script: {e}")
            return

    # Register in Windows Registry for Auto-Start
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "SystemMonitorService"
    
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, key_name, 0, reg.REG_SZ, f'pythonw.exe "{dest_script}"')
        print("✅ Persistence Installed: Will survive reboot.")
    except Exception as e:
        print(f"❌ Error installing persistence: {e}")

if __name__ == "__main__":
    install_persistence()
