from modules import agent_core
from modules.tools import system_control
import time

# Each case includes expected process image names to kill after launch
cases = [
    {"tool": "open_application", "args": {"name": "notepad"}, "kill": ["notepad.exe"]},
    {"tool": "open_application", "args": {"application": "Calculator"}, "kill": ["Calculator.exe", "calc.exe"]},
    {"tool": "open_application", "args": {"program": "chrome"}, "kill": ["chrome.exe"]},
    {"tool": "open_application", "args": {"app": "code"}, "kill": ["Code.exe", "code.exe"]},
    {"tool": "open_application", "args": {"application_name": "firefox"}, "kill": ["firefox.exe"]},
    # Passing args as a raw string (edge-case)
    {"tool": "open_application", "args": "vscode", "kill": ["Code.exe", "code.exe", "vscode.exe"]},
]

for i, case in enumerate(cases, 1):
    print(f"\n--- Test case {i}: {case}\n")
    try:
        res = agent_core.execute_tool(case["tool"], case["args"])
        print("Result:", res)

        # Give the app a moment to start before attempting to close it
        time.sleep(2)

        # Attempt to kill expected processes (best-effort)
        kill_results = []
        for proc in case.get("kill", []):
            kr = system_control.kill_process(proc)
            kill_results.append((proc, kr))

        print("Kill results:")
        for proc, kr in kill_results:
            print(f" - {proc}: {kr}")

    except Exception as e:
        print("Exception:", e)

print("\nDone tests.")
