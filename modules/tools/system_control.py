# tools/system_control.py
import subprocess
import os
import webbrowser
import sys
from pathlib import Path
import platform

def open_program(program_name):
    """Open programs by name"""
    program_name = str(program_name).lower().strip()
    
    programs = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "paint": "mspaint.exe",
        "task manager": "taskmgr.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "vs code": "code.exe",
        "visual studio code": "code.exe",
        "settings": "ms-settings:",
        "discord": "discord.exe",
        "spotify": "spotify.exe",
        "steam": "steam.exe"
    }
    
    try:
        if program_name in programs:
            executable = programs[program_name]
            if executable.startswith("ms-"):
                subprocess.run(f"start {executable}", shell=True)
            else:
                subprocess.Popen(executable)
            return f"✅ Opened {program_name}"
        else:
            subprocess.run(f"start {program_name}", shell=True)
            return f"✅ Attempted to open {program_name}"
    except Exception as e:
        return f"❌ Could not open {program_name}: {str(e)}"

def search_web(query):
    """Search the web"""
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"✅ Searched for: {query}"
    except Exception as e:
        return f"❌ Could not search: {str(e)}"

def open_folder(path):
    """Open folder in explorer"""
    try:
        if os.path.exists(path):
            subprocess.run(f'explorer "{path}"', shell=True)
            return f"✅ Opened folder: {path}"
        else:
            return f"❌ Folder not found: {path}"
    except Exception as e:
        return f"❌ Could not open folder: {str(e)}"

def install_package(package_name):
    """Install Python packages"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Successfully installed {package_name}"
        else:
            return f"❌ Failed to install {package_name}: {result.stderr}"
    except Exception as e:
        return f"❌ Installation error: {str(e)}"

def execute_command(command):
    """Execute system commands (USE WITH CAUTION)"""
    try:
        # Safety check - don't allow dangerous commands
        dangerous_commands = ['rm -rf', 'del /f', 'format', 'shutdown', 'reboot']
        if any(danger in command.lower() for danger in dangerous_commands):
            return f"❌ Dangerous command blocked: {command}"
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = f"Exit code: {result.returncode}\n"
        if result.stdout:
            output += f"Output:\n{result.stdout}\n"
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        return output
    except subprocess.TimeoutExpired:
        return "❌ Command timed out (30s limit)"
    except Exception as e:
        return f"❌ Command failed: {str(e)}"

def restart_program():
    """Restart the current Python program"""
    try:
        python = sys.executable
        script = sys.argv[0]
        subprocess.Popen([python, script])
        return "✅ Restarting program..."
    except Exception as e:
        return f"❌ Restart failed: {str(e)}"

def list_processes():
    """List running processes"""
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        return result.stdout[:2000]  # Limit output
    except Exception as e:
        return f"❌ Could not list processes: {str(e)}"

def kill_process(process_name):
    """Kill a process by name"""
    try:
        result = subprocess.run(['taskkill', '/f', '/im', process_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Killed process: {process_name}"
        else:
            return f"❌ Could not kill {process_name}: {result.stderr}"
    except Exception as e:
        return f"❌ Error killing process: {str(e)}"

def open_application(app_name):  # This should match what agent_core.py calls
    """Open an application using the most reliable method."""
    
    if platform.system() == "Windows":
        # Map app names to working commands
        app_commands = {
            "word": "start winword",
            "microsoft word": "start winword",
            "winword": "start winword",
            "excel": "start excel", 
            "microsoft excel": "start excel",
            "notepad": "start notepad",
            "calculator": "start calc",
            "calc": "start calc",
            "chrome": "start chrome",
            "firefox": "start firefox",
            "browser": "start chrome",
        }
        
        # Get the command for this app
        app_lower = app_name.lower()
        command = app_commands.get(app_lower, f"start {app_name}")
        
        try:
            print(f"🚀 Executing: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if result.returncode == 0:
                return f"✅ Successfully opened {app_name}"
            else:
                return f"❌ Failed to open {app_name}. Error: {result.stderr}"
                
        except Exception as e:
            return f"❌ Exception opening {app_name}: {str(e)}"
    
    return f"❌ Unsupported platform"