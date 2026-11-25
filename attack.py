import sys
import os
import subprocess
import ctypes
import importlib.util

def is_admin():
    """Check if the current process has admin rights."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """Re-launch the script with admin privileges."""
    print("[*] Not running as admin. Relaunching with elevated privileges...")
    
    # Get the current script path
    script_path = os.path.abspath(__file__)
    
    # Use shell32.dll to trigger UAC elevation
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        f'"{script_path}"', 
        None, 
        1
    )
    sys.exit(0)  # Exit the non-admin instance

def ensure_pywinauto():
    """Install pywinauto if not present."""
    spec = importlib.util.find_spec("pywinauto")
    if spec is None:
        print("[*] Installing pywinauto...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywinauto"])
        print("[+] pywinauto installed.")
    else:
        print("[+] pywinauto already installed.")

def attack_edge_tabs():
    """
    Forces Microsoft Edge to open and close tabs rapidly.
    """
    print("[*] Starting Edge Tab Attack...")
    
    try:
        # Connect to an existing Edge instance or launch a new one
        try:
            app = Application(backend="uia").connect(title_re=".*Microsoft Edge.*", timeout=5)
            print("[+] Connected to existing Edge window.")
        except Exception:
            # If no window is found, launch Edge
            import subprocess
            subprocess.Popen(["msedge"])
            time.sleep(2)  # Wait for Edge to fully load
            app = Application(backend="uia").connect(title_re=".*Microsoft Edge.*", timeout=10)
            print("[+] Launched new Edge window.")

        # Get the main window
        edge_window = app.window(title_re=".*Microsoft Edge.*")
        edge_window.wait('ready', timeout=10)
        
        # Focus the window to ensure clicks are registered correctly
        edge_window.set_focus()
        
        print("[*] Targeting Edge Tab Bar...")
        
        # We will simulate opening/closing by using keyboard shortcuts 
        # which are more reliable across different UI versions than mouse clicks.
        # Ctrl+T opens a new tab.
        # Ctrl+W closes the active tab.
        
        iterations = 20  # Number of open/close cycles
        
        for i in range(iterations):
            # Open a new tab
            send_keys('^t')  # Ctrl+T
            time.sleep(random.uniform(0.1, 0.3))
            
            # Close the tab
            send_keys('^w')  # Ctrl+W
            time.sleep(random.uniform(0.1, 0.3))
            
            if (i + 1) % 5 == 0:
                print(f"[+] Completed {i + 1} cycles.")

        print("[*] Attack completed. Closing Edge.")
        # Optional: Close Edge at the end
        # edge_window.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    # Step 1: Ensure we have admin rights
    if not is_admin():
        run_as_admin()
    
    # Step 2: Install dependencies if needed
    ensure_pywinauto()
    
    # Step 3: Run the attack
    attack_edge_tabs()
