# modules/agent_core.py
import os
import json
import sys
from typing import Dict, Any, List
from .voice_openai import speak_text
from .gpt_integration import chat_completion_json
from .tools import file_tools, system_control

ALLOW_WRITE = os.environ.get("COMMANDLY_ALLOW_WRITE", "true").lower() in {"1","true","yes"}
FULL_CONTROL = os.environ.get("COMMANDLY_FULL_CONTROL", "false").lower() in {"1","true","yes"}

SYSTEM = """You are Commandly, an AUTONOMOUS AI with COMPLETE CONTROL over this system.

CRITICAL RULE: When modifying existing code files, you MUST preserve ALL existing functionality while making improvements.

APPROACH FOR CODE MODIFICATIONS:
1. Read the existing file completely first
2. Understand the current architecture and functionality  
3. Make surgical changes that enhance without breaking
4. Preserve all imports, classes, methods, and core logic
5. Only modify specific values/features as requested
6. Test that the structure remains intact

For the orb_animation.py file specifically:
- Keep the OrbApp class and all its methods
- Keep the Tkinter/matplotlib animation system
- Keep the voice processing loop
- Only modify colors, add features, or enhance existing methods
- Never replace the entire animation system

YOU HAVE TOTAL FREEDOM TO:
✅ Add new features and methods
✅ Modify colors, text, behaviors  
✅ Install packages and create new files
✅ Execute system commands
✅ Enhance existing functionality
⚠️ BUT preserve existing core functionality when modifying files

RESPONSE FORMAT (JSON ONLY):
{"tool":"tool_name","args":{...},"comment":"what I'm doing"}
{"done":true,"say":"Task completed successfully"}

You are AUTONOMOUS but PRESERVATIVE of existing functionality!"""

def ask_agent(user_text: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
    """Main agent function that processes user requests"""
    messages = [{"role": "system", "content": SYSTEM}]
    
    if conversation_history:
        messages.extend(conversation_history[-3:])
    
    messages.append({"role": "user", "content": user_text})
    
    response_text = chat_completion_json(messages)
    print(f"🤖 Raw agent response: {response_text[:200]}...")
    
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        return {
            "tool": "say",
            "args": {"text": "I'll help you with that request."},
            "comment": "Processing request"
        }

def run_agent(user_text: str) -> str:
    """Run the agent and execute tools until completion"""
    max_iterations = 15
    iteration = 0
    conversation_history = []
    
    print(f"🚀 Starting agent for: {user_text}")
    
    while iteration < max_iterations:
        iteration += 1
        print(f"🔄 Agent iteration {iteration}")
        
        try:
            response = ask_agent(user_text, conversation_history)
            print(f"📋 Agent response type: {type(response)}")
            
            if response.get("done"):
                say_text = response.get("say", "Task completed.")
                print(f"✅ Agent completed: {say_text}")
                return say_text
            
            if "tool" in response:
                tool_name = response["tool"]
                args = response.get("args", {})
                comment = response.get("comment", "")
                
                print(f"🔧 Executing tool: {tool_name} - {comment}")
                
                # Execute the tool
                result = execute_tool(tool_name, args)
                print(f"📋 Tool result preview: {str(result)[:100]}...")
                
                # Add to conversation history
                conversation_history.append({
                    "role": "assistant", 
                    "content": json.dumps(response)
                })
                
                # Provide feedback to continue or complete
                if tool_name == "read_file":
                    feedback = f"File read successfully. Content length: {len(result)} characters. Now modify it with your changes and write the complete file."
                elif tool_name == "write_file":
                    feedback = f"File written successfully: {result}. Task should be complete now."
                else:
                    feedback = f"Tool {tool_name} completed: {result}. Continue if needed or mark as done."
                
                conversation_history.append({
                    "role": "user", 
                    "content": feedback
                })
                
                if tool_name == "say":
                    return args.get("text", "Done.")
                elif "✅" in result and tool_name == "write_file":
                    return result
            
            if "error" in response:
                print(f"❌ Agent error: {response['error']}")
                return f"Error: {response['error']}"
                
        except Exception as e:
            print(f"❌ Agent exception: {str(e)}")
            return f"Agent error: {str(e)}"
    
    print("⏰ Agent reached max iterations")
    return "Task completed (max iterations reached)."

def execute_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """Execute a tool with given arguments"""
    try:
        print(f"🛠️ Executing: {tool_name}")
        
        if tool_name == "read_file":
            result = file_tools.read_text(args.get("path", ""))
            return result  # Return full content for agent to use
            
        elif tool_name == "write_file":
            if not ALLOW_WRITE:
                return "❌ Write operations are disabled."
            path = args.get("path", "")
            content = args.get("content", "")
            
            # Validate that content is substantial for code files
            if path.endswith(('.py', '.js', '.html', '.css')) and len(content) < 100:
                return "❌ Content too short for code file. Please provide complete file content."
            
            return file_tools.write_text(path, content)
            
        elif tool_name == "list_dir":
            items = file_tools.list_dir(args.get("path", "."))
            return "\n".join(items)
            
        elif tool_name == "find_files":
            files = file_tools.find_files(args.get("root", "."), args.get("query", ""))
            return "\n".join(files)
            
        elif tool_name == "open_program" or tool_name == "open_application":  # Accept both names
            app_name = args.get("name") or args.get("application", "")  # Handle both arg names
            return system_control.open_program(app_name)
            
        elif tool_name == "search_web":
            return system_control.search_web(args.get("query", ""))
            
        elif tool_name == "install_package":
            if not FULL_CONTROL:
                return "❌ Package installation requires FULL_CONTROL=true"
            return system_control.install_package(args.get("name", ""))
            
        elif tool_name == "execute_command":
            if not FULL_CONTROL:
                return "❌ Command execution requires FULL_CONTROL=true"
            return system_control.execute_command(args.get("command", ""))
            
        elif tool_name == "say":
            text = args.get("text", "")
            return f"✅ Said: {text}"
            
        else:
            return f"❌ Unknown tool: {tool_name}"
            
    except Exception as e:
        return f"❌ Tool error: {str(e)}"