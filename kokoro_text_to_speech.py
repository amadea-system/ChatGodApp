import os
import random
# import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI
from gtts import gTTS
from pydub import AudioSegment
import pygame

from dotenv import load_dotenv
load_dotenv()

# AZURE_VOICES = [
#     "en-US-DavisNeural",
#     "en-US-TonyNeural",
#     "en-US-JasonNeural",
#     "en-US-GuyNeural",
#     "en-US-JaneNeural",
#     "en-US-NancyNeural",
#     "en-US-JennyNeural",
#     "en-US-AriaNeural",
# ]

# AZURE_VOICE_STYLES = [
#     # Currently using the 9 of the 11 available voice styles
#     # Note that certain styles aren't available on all voices
#     "angry",
#     "cheerful",
#     "excited",
#     "hopeful",
#     "sad",
#     "shouting",
#     "terrified",
#     "unfriendly",
#     "whispering"
# ]

# AZURE_PREFIXES = {
#     "(angry)" : "angry",
#     "(cheerful)" : "cheerful",
#     "(excited)" : "excited",
#     "(hopeful)" : "hopeful",
#     "(sad)" : "sad",
#     "(shouting)" : "shouting",
#     "(shout)" : "shouting",
#     "(terrified)" : "terrified",
#     "(unfriendly)" : "unfriendly",
#     "(whispering)" : "whispering",
#     "(whisper)" : "whispering",
#     "(random)" : "random"
# }

# KOKORO_VOICES = [
#     "af_heart",
#     "af_alloy",
#     "af_aoede",
#     "af_bella",
#     "af_jessica",
#     "af_kore ",
#     "af_nicole",
#     "af_nova",
#     "af_river",
#     "af_sarah",
#     "af_sky",
#     "am_adam",
#     "am_echo",
#     "am_eric",
#     "am_fenrir",
#     "am_liam",
#     "am_michael",
#     "am_onyx",
#     "am_puck",
#     "am_santa",
#     "bf_alice",
#     "bf_emma",
#     "bf_isabella",
#     "bf_lily",
#     "bm_daniel",
#     "bm_fable",
#     "bm_george",
#     "bm_lewis",
# ]


KOKORO_VOICES = [
    "af_alloy",
    "af_aoede",
    "af_bella",
    "af_heart",
    "af_jadzia",
    "af_jessica",
    "af_kore",
    "af_nicole",
    "af_nova",
    "af_river",
    "af_sarah",
    "af_sky",
    "af_v0",
    "af_v0bella",
    "af_v0irulan",
    "af_v0nicole",
    "af_v0sarah",
    "af_v0sky",
    "am_adam",
    "am_echo",
    "am_eric",
    "am_fenrir",
    "am_liam",
    "am_michael",
    "am_onyx",
    "am_puck",
    "am_santa",
    "am_v0adam",
    "am_v0gurney",
    "am_v0michael",
    "bf_alice",
    "bf_emma",
    "bf_lily",
    "bf_v0emma",
    "bf_v0isabella",
    "bm_daniel",
    "bm_fable",
    "bm_george",
    "bm_lewis",
    "bm_v0george",
    "bm_v0lewis"
]

class KokoroTTSManager:
    # azure_speechconfig = None
    # azure_synthesizer = None
    kokoro_client = None

    def __init__(self):
        pygame.init()
        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        # self.azure_speechconfig = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_TTS_KEY'), region=os.getenv('AZURE_TTS_REGION'))
        # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
        # self.azure_speechconfig.speech_synthesis_voice_name = "en-US-AriaNeural"
        # Creates a speech synthesizer. Setting audio_config to None means it wont play the synthesized text out loud.
        # self.azure_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.azure_speechconfig, audio_config=None)        

        print("Connecting to Kokoro TTS API...")
        if os.getenv('KOKORO_TTS_URL') is None or os.getenv('KOKORO_TTS_KEY') is None:
            raise ValueError("KOKORO_TTS_URL and KOKORO_TTS_KEY must be set in the environment variables.")

        self.kokoro_client = OpenAI(base_url=os.getenv('KOKORO_TTS_URL'), api_key=os.getenv('KOKORO_TTS_KEY'))

    # Returns the path to the new .wav file
    def text_to_audio(self, text: str, voice_name="random", voice_style="random"):
        if voice_name == "random":
            voice_name = random.choice(KOKORO_VOICES)
        # if voice_style == "random":
        #     voice_style = random.choice(AZURE_VOICE_STYLES)

        # Change the voice style if the message includes a prefix
        text = text.lower()
        # if text.startswith("(") and ")" in text:
        #     prefix = text[0:(text.find(")")+1)]
        #     if prefix in AZURE_PREFIXES:
        #         voice_style = AZURE_PREFIXES[prefix]
        #         text = text.removeprefix(prefix)
        if len(text) == 0:
            print("This message was empty")
            return
        
        # if voice_style == "random":
        #     voice_style = random.choice(AZURE_VOICE_STYLES)

        # ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='en-US'><voice name='{voice_name}'><mstts:express-as style='{voice_style}'>{text}</mstts:express-as></voice></speak>"
        # result = self.azure_synthesizer.speak_ssml_async(ssml_text).get()

        # output = os.path.join(os.path.abspath(os.curdir), f"_Msg{str(hash(text))}{str(hash(voice_name))}{str(hash(voice_style))}.wav")
        # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #     stream = speechsdk.AudioDataStream(result)
        #     stream.save_to_wav_file(output)
        # else:
        #     # If Azure fails, use gTTS instead. gTTS saves as an mp3 by default, so convert it to a wav file after
        #     print("\n   Azure failed, using gTTS instead   \n")
        #     output_mp3 = output.replace(".wav", ".mp3")
        #     msgAudio = gTTS(text=text, lang='en', slow=False)
        #     msgAudio.save(output_mp3)
        #     audiosegment = AudioSegment.from_mp3(output_mp3)
        #     audiosegment.export(output, format="wav")

        output = os.path.join(os.path.abspath(os.curdir), f"_Msg{str(hash(text))}{str(hash(voice_name))}.wav")
        output_mp3 = output.replace(".mp3", ".wav")

        try:
            with self.kokoro_client.audio.speech.with_streaming_response.create(
                model="kokoro",
                voice=voice_name,
                input=text,
                # format="wav"
            ) as response:
                response.stream_to_file(output_mp3)
        except Exception as e:
            print(f"Error generating audio: {e}")
            print("\n   Kokoro failed, using gTTS instead   \n")
            msgAudio = gTTS(text=text, lang='en', slow=False)
            msgAudio.save(output_mp3)

        audiosegment = AudioSegment.from_mp3(output_mp3)
        audiosegment.export(output, format="wav")
    
        return output


# Tests here
if __name__ == '__main__':
    tts_manager = KokoroTTSManager()
    pygame.mixer.init()

    print(f"Voice: {KOKORO_VOICES[0]}")
    file_path = tts_manager.text_to_audio("Here's my test audio!!", KOKORO_VOICES[0])
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    voice_number = 0

    while True:
        stuff_to_say = input("\nNext question? \n\n")
        if len(stuff_to_say) == 0:
            continue
        # voice_number = (voice_number + 1) % len(KOKORO_VOICES)
        voice_number = (voice_number + 1)
        next_voice = KOKORO_VOICES[voice_number]
        print(f"Voice: {next_voice}")
        file_path = tts_manager.text_to_audio(stuff_to_say, next_voice)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
