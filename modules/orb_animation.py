# modules/orb_animation.py
import tkinter as tk
import textwrap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import sys
import os
import pyaudio # Add this import for testing audio devices

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.gpt_integration import ask_gpt, decide_mode
from modules.agent_core import run_agent
from modules.voice_openai import record_audio, transcribe_audio, speak_text

class OrbApp(tk.Tk):
    ###############################################################################
    #### main frame ####
    ###############################################################################

    # Initialize the application calling TK window and add simple UI parameters.
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Commandly Orb")
        self.geometry("600x700")
        self.configure(bg='black')
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Determine the center position for the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - 600) / 2)
        y = int((screen_height - 700) / 2)
        self.geometry(f"+{x}+{y}")

        # Dragging functionality key binding.
        self.bind("<ButtonPress-1>", self.start_move)#<--
        self.bind("<B1-Motion>", self.do_move)#<--

        ###############################################################################
        #### end main frame ####
        ###############################################################################


        
        ####################
        # Status frame.
        self.status_frame = tk.Frame(self, width=500, height=400, bg="black")
        self.status_frame.grid(row=0, column=0)
        self.status_label = tk.Label(self.status_frame, text="🧪 Status", fg="white", bg="black", font=("Consolas", 14, "bold"))
        self.status_label.pack(pady=5)
        self.grid_rowconfigure(1, weight=0) # anti_orb distortion.


        #####################
        # Orb animation frame.
        self.orb_frame = tk.Frame(
            self,
            width=100,
            height=100,
            bg="black")

        # Orb positioned in second row and size fixed.
        self.orb_frame.grid(row=1, column=0)
        self.orb_frame.grid_propagate(False)

        # Display the orb animation
        self.canvas = self.setup_orb_animation() # <--
        

        # Chat frame for text display.
        self.chat_frame = tk.Frame(self, height=120, bg="black")
        self.chat_frame.grid(row=2, column=0)
        self.text_canvas = tk.Canvas(self.chat_frame, width=600, height=120, bg="black", highlightthickness=0)
        self.text_canvas.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Complete the line
        self.grid_columnconfigure(0, weight=1)
        

        self.system_prompt = self.load_system_prompt() # <--
        self.conversation = [{"role": "system", "content": self.system_prompt}]

        # Initialize mode and lock thread.
        self.mode = "idle"
        self.lock = threading.Lock()

        threading.Thread(target=self.assistant_loop, daemon=True).start()#<--

        # Test audio devices - Add this test to your code temporarily
        self.test_audio_devices()

    def test_audio_devices(self):
        p = pyaudio.PyAudio()
        print(f"Audio devices found: {p.get_device_count()}")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"Microphone {i}: {info['name']}")
        




############################################################################################################################
### Method definitions.
############################################################################################################################

    # Dragging functionality.
    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self._drag_start_x
        y = self.winfo_y() + event.y - self._drag_start_y
        self.geometry(f"+{x}+{y}")




    # Declaring rings for animation. x list and y list
    def init_rings(self):
        for ring in self.rings:
            ring.set_data([], [])
        return self.rings



    def setup_orb_animation(self):

        # Plot Matplotlib figure and subplots containing the orb animation.
        fig = plt.Figure(figsize=(1, 1), facecolor='black', dpi=100)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.set_facecolor('black')
        ax.set_xlim(-0.15, 0.15)
        ax.set_ylim(-0.15, 0.15)
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)



        ####################
        # Orb animation parameters.
        self.num_rings = 6
        self.base_radius = 0.0006
        self.ring_spacing = 0.004
        self.breathing_speed = 2
        self.shrinkage_scale = 0.002

        # Create rings for the animation.
        self.rings = []
        for _ in range(self.num_rings):
            ring, = ax.plot([], [], lw=1.2, alpha=0.8)
            self.rings.append(ring)



        ##Embed matplotlib figure in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.orb_frame)
        canvas.get_tk_widget().pack(padx=5, pady=5)

        # breathing animation
        self.anim = animation.FuncAnimation(
            fig, self.animate, init_func=self.init_rings, frames=500, interval=30, blit=True
        )
        return canvas

    # breathing animation 
    def animate(self, frame):
        t = frame / 20.0
        color = self.get_color_for_mode()
        for i, ring in enumerate(self.rings):
            radius_variation = self.shrinkage_scale * np.sin(t * self.breathing_speed - i * 0.4)
            radius = self.base_radius + i * self.ring_spacing + radius_variation
            theta = np.linspace(0, 2 * np.pi, 200)
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            ring.set_data(x, y)
            ring.set_color(color)
        return self.rings






    def get_color_for_mode(self):
        with self.lock:
            mode = self.mode
        return {
            "idle": "#FF0000",  # Red color
            "listening": "#3399ff",
            "thinking": "#ffd700", 
            "speaking": "#00cc66",
            "agent": "#ff6600"
        }.get(mode, "#FF0000")







    def set_mode(self, mode):
        with self.lock:
            self.mode = mode









    def update_text(self, user_input, reply):
        self.text_canvas.delete("all")
        wrapped_user = textwrap.fill(f"You: {user_input}", width=40)
        wrapped_reply = textwrap.fill(f"Commandly: {reply}", width=40)
        self.text_canvas.create_text(300, -5, anchor="n", fill="white", font=("Consolas", 12),
                                     text=wrapped_user, justify="center")
        self.text_canvas.create_text(300, 25, anchor="n", fill="white", font=("Consolas", 12),
                                     text=wrapped_reply, justify="center")







    def update_status(self, message):
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)







    def load_system_prompt(self, filepath=".commandly_prompt.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "You are Commandly, an autonomous assistant that can modify files and execute system commands."








    def assistant_loop(self):
        print("🧠 Assistant is running with Orb UI.")
        while True:
            try:
                self.set_mode("listening")
                self.update_status("🎙️ Listening...")
                
                has_audio = record_audio()
                
                if not has_audio:
                    print("🔇 No audio detected, continuing to listen...")
                    time.sleep(0.5)
                    continue

                self.set_mode("thinking")
                self.update_status("🧠 Transcribing...")
                user_input = transcribe_audio()
                
            except Exception as e:
                self.update_status("⚠️ Voice input failed. Type instead.")
                print(f"⚠️ Voice input unavailable ({e}). Please type your input.")
                try:
                    user_input = input("You: ")
                except (EOFError, KeyboardInterrupt):
                    print("👋 Goodbye!")
                    self.destroy()
                    break
                self.set_mode("thinking")

            if not user_input or len(user_input.strip()) < 2:
                print("🔇 No meaningful input detected, continuing to listen...")
                self.set_mode("idle")
                self.update_status("🎤 Ready to listen...")
                time.sleep(0.5)
                continue

            exit_commands = ["exit", "quit", "stop", "goodbye", "bye", "close", "shut down", "end"]
            if any(cmd in user_input.lower() for cmd in exit_commands):
                try:
                    self.set_mode("speaking")
                    self.update_status("👋 Exiting...")
                    speak_text("Goodbye!")
                    print("👋 Goodbye!")
                except:
                    print("👋 Goodbye!")
                self.destroy()
                break

            print(f"🗣️ Processing: '{user_input}'")
            
            mode = decide_mode(user_input)
            
            if mode == "agent":
                self.set_mode("agent")
                self.update_status("🔧 Agent mode - Executing...")
                try:
                    reply = run_agent(user_input)
                except Exception as e:
                    reply = f"Agent error: {str(e)}"
            else:
                self.conversation.append({"role": "user", "content": user_input})
                self.update_status("🤖 Thinking...")
                reply = ask_gpt(self.conversation)
                self.conversation.append({"role": "assistant", "content": reply})

            print("Commandly:", reply)
            self.update_text(user_input, reply)

            try:
                self.set_mode("speaking")
                self.update_status("💬 Speaking...")
                speak_text(reply)
            except Exception as e:
                print(f"⚠️ Voice output unavailable ({e}).")
                print("Commandly (text):", reply)

            self.set_mode("idle")
            self.update_status("✅ Ready")
            time.sleep(0.1)

if __name__ == "__main__":
    app = OrbApp()
    app.mainloop()