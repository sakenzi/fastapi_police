import whisper
import warnings


class Transcribe:
    def __init__(self):
        self.model = whisper.load_model("base")

    def audio(self, audio_file: str) -> str:
        result = self.model.transcribe(audio=audio_file, fp16=False)
        return result["text"]
    
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")

transcriber = Transcribe()