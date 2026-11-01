import os
import re
import soundfile as sf
from typing import List
from pipeline.models import SceneBeat, ProjectConfig

def clean_script_line(text: str) -> str:
    cleaned = re.sub(r"\[.*?\]", "", text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def generate_master_voice(
    beats: List[SceneBeat],
    config: ProjectConfig,
    audio_dir: str
) -> List[SceneBeat]:
    """
    Generates a single, continuous Master Audio narration for the entire script at once.
    - Preserves natural, uninterrupted breathing cadence and momentum.
    - Eliminates slicing and artificial silences.
    - Saves master audio to audio/master_narration.wav.
    """
    os.makedirs(audio_dir, exist_ok=True)
    master_filename = "master_narration.wav"
    out_path = os.path.join(audio_dir, master_filename).replace("\\", "/")

    # Combine all beats into continuous script text
    cleaned_sentences = []
    for beat in beats:
        clean_text = clean_script_line(beat.spoken_text)
        beat.spoken_text = clean_text
        beat.audio_file = master_filename
        beat.audio_path = out_path
        if clean_text:
            cleaned_sentences.append(clean_text)

    full_text = " ".join(cleaned_sentences)

    print(f"[VoiceEngine] Initializing VieNeu-TTS (Voice: {config.voice_name})...")
    from vieneu import Vieneu
    tts = Vieneu()

    print(f"[VoiceEngine] Synthesizing continuous Master Narration ({len(beats)} scenes, {len(full_text.split())} words)...")
    raw_audio = tts.infer(full_text, voice=config.voice_name, temperature=0.7)
    sr = 48000

    # Save 48kHz Master Audio
    sf.write(out_path, raw_audio, sr)

    total_dur_sec = len(raw_audio) / sr
    total_frames = int(round(total_dur_sec * config.fps))

    print(f"[VoiceEngine] Master Audio generated successfully:")
    print(f"  - Output: {out_path}")
    print(f"  - Duration: {total_dur_sec:.2f}s ({total_frames} frames @ {config.fps} FPS)")

    return beats
