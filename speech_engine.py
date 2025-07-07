import os

class SpeechEngine:
    def __init__(self, voice="tr", speed=140):
        self.voice = voice
        self.speed = speed

    def speak(self, text):
        command = f'espeak -v {self.voice} -s {self.speed} "{text}"'
        os.system(command)
