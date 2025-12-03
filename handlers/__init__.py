from .audio import register_audio_handlers
from .start import register_start_handlers
from .tts import register_tts_handlers

__all__ = ["register_audio_handlers", "register_start_handlers", "register_tts_handlers"]
