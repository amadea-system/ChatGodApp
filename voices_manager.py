from audio_player import AudioManager

import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv('ENABLE_OBS_WEBSOCKETS') == 'true':
    from obs_websockets import OBSWebsocketsManager
else:
    OBSWebsocketsManager = None

SpeechEngine = None
if os.getenv('SPEECH_ENGINE') == 'azure':
    from azure_text_to_speech import AzureTTSManager
    SpeechEngine = AzureTTSManager
elif os.getenv('SPEECH_ENGINE') == 'kokoro':
    from kokoro_text_to_speech import KokoroTTSManager
    SpeechEngine = KokoroTTSManager
else:
    raise ValueError("SPEECH_ENGINE must be set to either 'azure' or 'kokoro' in the environment variables.")

class TTSManager:
    tts_speech_engine = SpeechEngine()
    audio_manager = AudioManager()
    obswebsockets_manager = OBSWebsocketsManager() if OBSWebsocketsManager else None

    # TODO: These voices are not available in Kokoro TTS, so they will need to be updated. Make Dynamic?
    user1_voice_name = "en-US-DavisNeural"
    user1_voice_style = "random"
    user2_voice_name = "en-US-TonyNeural"
    user2_voice_style = "random"
    user3_voice_name = "en-US-JaneNeural"
    user3_voice_style = "random"

    def __init__(self):
        file_path = self.tts_speech_engine.text_to_audio("Chat God App is now running!") # Say some shit when the app starts
        self.audio_manager.play_audio(file_path, True, True, True)

    def update_voice_name(self, user_number, voice_name):
        if user_number == "1":
            self.user1_voice_name = voice_name
        elif user_number == "2":
            self.user2_voice_name = voice_name
        elif user_number == "3":
            self.user3_voice_name = voice_name
        
    def update_voice_style(self, user_number, voice_style):
        if user_number == "1":
            self.user1_voice_style = voice_style
        elif user_number == "2":
            self.user2_voice_style = voice_style
        elif user_number == "3":
            self.user3_voice_style = voice_style

    def text_to_audio(self, text, user_number):
        if user_number == "1":
            voice_name = self.user1_voice_name
            voice_style = self.user1_voice_style
        elif user_number == "2":
            voice_name = self.user2_voice_name
            voice_style = self.user2_voice_style
        elif user_number == "3":
            voice_name = self.user3_voice_name
            voice_style = self.user3_voice_style

        tts_file = self.tts_speech_engine.text_to_audio(text, voice_name, voice_style)

        # OPTIONAL: Use OBS Websockets to enable the Move plugin filter
        if self.obswebsockets_manager is not None:
            if user_number == "1":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 1", True)
            elif user_number == "2":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 2", True)
            elif user_number == "3":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 3", True)

        self.audio_manager.play_audio(tts_file, True, True, True)

        if self.obswebsockets_manager is not None:
            if user_number == "1":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 1", False)
            elif user_number == "2":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 2", False)
            elif user_number == "3":
                self.obswebsockets_manager.set_filter_visibility("Line In", "Audio Move - DnD Player 3", False)
