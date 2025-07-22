from gtts import gTTS
import os
import uuid
import re

def clean_text_for_tts(text: str) -> str:
    # Remove markdown symbols: **, __, ##, --, etc.
    text = re.sub(r'[*_#`>-]+', '', text)
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def text_to_audio_autoplay(text: str, lang: str = "en", return_path=False):
    try:
        audio_dir = "audio"
        os.makedirs(audio_dir, exist_ok=True)

        # Remove old audio files
        for f in os.listdir(audio_dir):
            if f.endswith(".mp3"):
                try:
                    os.remove(os.path.join(audio_dir, f))
                except Exception:
                    pass

        # Clean markdown artifacts from the text
        cleaned_text = clean_text_for_tts(text)

        # Generate new filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(audio_dir, filename)

        # Convert to speech
        tts = gTTS(text=cleaned_text, lang=lang)
        tts.save(filepath)

        if return_path:
            return filepath, filename

        # Fallback: HTML autoplay
        audio_url = f"/audio/{filename}"
        return f"""
        <audio autoplay controls>
          <source src="{audio_url}" type="audio/mp3">
          Your browser does not support the audio element.
        </audio>
        """
    except Exception as e:
        return f"[TTS Error] {str(e)}"
