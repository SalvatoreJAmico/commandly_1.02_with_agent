# modules/voice_openai.py
import pyaudio
import wave
import openai
import os
import time
import pygame
import numpy as np
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_audio(filename="user_input.wav", duration=5, silence_threshold=1000):
    """Record audio with silence detection"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("🎤 Speak now...")
    frames = []
    silence_count = 0
    max_silence = int(RATE / CHUNK * 1.5)  # 1.5 seconds of silence
    speech_detected = False

    for i in range(int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
        
        # Check audio level for silence detection
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_level = np.abs(audio_data).mean()
        
        # If we detect speech (above threshold)
        if audio_level > silence_threshold:
            speech_detected = True
            silence_count = 0
        else:
            silence_count += 1
        
        # If we detected speech and then silence, stop recording
        if speech_detected and silence_count > max_silence:
            print("🔇 Silence after speech detected, stopping recording...")
            break

    print("✅ Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Only save if we detected actual speech
    if speech_detected and len(frames) > 10:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        return True
    else:
        print("⚠️ No speech detected")
        return False

def transcribe_audio(filename="user_input.wav"):
    """Send to Whisper for transcription with better filtering"""
    try:
        # Check if file exists and has content
        if not os.path.exists(filename) or os.path.getsize(filename) < 5000:
            return ""
        
        with open(filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"  # Force English to reduce phantom phrases
            )
        
        text = transcript.text.strip()
        
        # Filter out common phantom phrases and background noise
        phantom_phrases = [
            "thank you", "thanks", "you", "bye", "goodbye", "mm-hmm", "uh-huh",
            "um", "uh", "oh", "ah", "okay", "ok", "yes", "no", "hello", "hi",
            "the", "a", "an", "and", "or", "but", "so", "well", "now", "then",
            "i", "me", "my", "we", "us", "our", "you", "your", "he", "she", "it",
            "they", "them", "their", "this", "that", "these", "those", "here", "there",
            "music", "sound", "noise", "background", "audio", "video", "youtube",
            "playing", "play", "song", "track", "volume", "speaker", "headphone"
        ]
        
        # Convert to lowercase for comparison
        text_lower = text.lower()
        
        # If the text is very short or just phantom phrases, ignore it
        words = text_lower.split()
        if len(words) <= 3 and all(word in phantom_phrases for word in words):
            print(f"🚫 Filtering phantom phrase: '{text}'")
            return ""
        
        # If it's too short and doesn't seem like a real command, ignore it
        if len(text) < 5:
            print(f"🚫 Text too short: '{text}'")
            return ""
        
        # Filter out common background noise transcriptions
        noise_patterns = [
            "music", "playing", "song", "audio", "video", "youtube", "sound",
            "background", "noise", "speaker", "headphone", "volume"
        ]
        
        if any(pattern in text_lower for pattern in noise_patterns) and len(words) < 5:
            print(f"🚫 Filtering background noise: '{text}'")
            return ""
        
        print(f"📝 Transcribed: '{text}'")
        return text
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return ""

def speak_text(text, voice="nova"):
    """Use OpenAI TTS to synthesize speech"""
    try:
        # Truncate text if it's too long
        if len(text) > 4000:
            text = text[:4000] + "..."
        
        filename = f"response_{int(time.time())}.mp3"

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        response.stream_to_file(filename)
        
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
        
        try:
            os.remove(filename)
        except:
            pass
            
    except Exception as e:
        print(f"Speech error: {str(e)}")

