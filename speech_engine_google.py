from gtts import gTTS
import pygame
import tempfile
import os
import time
class GTTSWrapper:
    def __init__(self, lang='tr'):
        self.lang = lang
        pygame.mixer.init()

    def speak(self, text):
        try:
            tts = gTTS(text=f" {text}", lang=self.lang, slow=False)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                tts.save(temp_file.name)
                temp_path = temp_file.name

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            # Ses bitene kadar bekle
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            time.sleep(0.1)
            os.unlink(temp_path)

        except Exception as e:
            print(f"[ERROR] gTTS failed: {e}")
