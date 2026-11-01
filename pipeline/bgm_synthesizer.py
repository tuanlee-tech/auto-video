import os
import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav

SR = 44100

def create_reverb_ir(duration=2.5, decay=3.0, sr=SR):
    samples = int(duration * sr)
    noise = np.random.randn(samples)
    envelope = np.exp(-decay * np.linspace(0, duration, samples))
    ir = noise * envelope
    return ir / np.max(np.abs(ir))

def apply_reverb(audio, ir):
    convolved = signal.fftconvolve(audio, ir, mode='full')[:len(audio)]
    return 0.7 * audio + 0.3 * convolved

def low_pass_filter(audio, cutoff, sr=SR):
    sos = signal.butter(4, cutoff, btype='low', fs=sr, output='sos')
    return signal.sosfilt(sos, audio)

def generate_pad_voice(freqs, duration, lfo_freq=0.1, detune_cents=8, sr=SR):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    voice = np.zeros_like(t)
    for f in freqs:
        f_detune_p = f * (2 ** (detune_cents / 1200))
        f_detune_m = f * (2 ** (-detune_cents / 1200))
        # Layer fundamentals and soft harmonics
        voice += 0.5 * np.sin(2 * np.pi * f * t)
        voice += 0.25 * np.sin(2 * np.pi * f_detune_p * t)
        voice += 0.25 * np.sin(2 * np.pi * f_detune_m * t)
        voice += 0.15 * np.sin(2 * np.pi * (2 * f) * t)
    
    # Apply slow breathing LFO
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * lfo_freq * t)
    return voice * lfo

def make_seamless_loop(audio, fade_len_sec=3.0, sr=SR):
    fade_samples = int(fade_len_sec * sr)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    # Crossfade head and tail
    head = audio[:fade_samples]
    tail = audio[-fade_samples:]
    crossfaded = tail * fade_out + head * fade_in
    audio[:fade_samples] = crossfaded
    return audio[:-fade_samples]

def synthesize_dark_suspense(duration=65, sr=SR):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # D minor: D2(73.4), A2(110.0), D3(146.8), F3(174.6), A3(220.0), C4(261.6)
    pad = generate_pad_voice([73.4, 110.0, 146.8, 174.6, 220.0], duration, lfo_freq=0.08, detune_cents=12, sr=sr)
    # Sub-bass pulse
    sub = 0.6 * np.sin(2 * np.pi * 36.7 * t) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t))
    # Filter
    pad = low_pass_filter(pad, 450, sr=sr)
    mix = pad + sub
    ir = create_reverb_ir(duration=3.0, decay=2.5, sr=sr)
    mix = apply_reverb(mix, ir)
    mix = make_seamless_loop(mix, fade_len_sec=4.0, sr=sr)
    return mix / np.max(np.abs(mix)) * 0.85

def synthesize_deep_contemplative(duration=65, sr=SR):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # A minor: A2(110.0), E3(164.8), A3(220.0), C4(261.6), E4(329.6)
    pad = generate_pad_voice([110.0, 164.8, 220.0, 261.6, 329.6], duration, lfo_freq=0.12, detune_cents=9, sr=sr)
    sub = 0.4 * np.sin(2 * np.pi * 55.0 * t)
    pad = low_pass_filter(pad, 750, sr=sr)
    mix = pad + sub
    ir = create_reverb_ir(duration=3.5, decay=2.0, sr=sr)
    mix = apply_reverb(mix, ir)
    mix = make_seamless_loop(mix, fade_len_sec=4.0, sr=sr)
    return mix / np.max(np.abs(mix)) * 0.85

def synthesize_hopeful_awakening(duration=65, sr=SR):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # C major / G: C3(130.8), G3(196.0), C4(261.6), E4(329.6), G4(392.0), B4(493.9)
    pad = generate_pad_voice([130.8, 196.0, 261.6, 329.6, 392.0], duration, lfo_freq=0.15, detune_cents=7, sr=sr)
    sub = 0.3 * np.sin(2 * np.pi * 65.4 * t)
    pad = low_pass_filter(pad, 1400, sr=sr)
    # Gentle sparkle harmonic
    sparkle = 0.1 * np.sin(2 * np.pi * 523.25 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t))
    mix = pad + sub + sparkle
    ir = create_reverb_ir(duration=2.8, decay=2.2, sr=sr)
    mix = apply_reverb(mix, ir)
    mix = make_seamless_loop(mix, fade_len_sec=4.0, sr=sr)
    return mix / np.max(np.abs(mix)) * 0.85

def synthesize_peaceful_minimal(duration=65, sr=SR):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # F maj7: F2(87.3), C3(130.8), F3(174.6), A3(220.0), C4(261.6), E4(329.6)
    pad = generate_pad_voice([87.3, 130.8, 174.6, 220.0, 261.6], duration, lfo_freq=0.09, detune_cents=6, sr=sr)
    sub = 0.4 * np.sin(2 * np.pi * 43.65 * t)
    pad = low_pass_filter(pad, 850, sr=sr)
    mix = pad + sub
    ir = create_reverb_ir(duration=3.2, decay=1.8, sr=sr)
    mix = apply_reverb(mix, ir)
    mix = make_seamless_loop(mix, fade_len_sec=4.0, sr=sr)
    return mix / np.max(np.abs(mix)) * 0.85

def generate_all_stock_bgm(output_dir="channels/common_assets/bgm"):
    os.makedirs(output_dir, exist_ok=True)
    tracks = [
        ("dark_suspense.wav", synthesize_dark_suspense),
        ("deep_contemplative.wav", synthesize_deep_contemplative),
        ("hopeful_awakening.wav", synthesize_hopeful_awakening),
        ("peaceful_minimal.wav", synthesize_peaceful_minimal),
    ]
    for filename, func in tracks:
        path = os.path.join(output_dir, filename)
        if not os.path.exists(path):
            print(f"[BGMSynthesizer] Generating {filename}...")
            audio = func(duration=65)
            wav.write(path, SR, (audio * 32767).astype(np.int16))
            print(f"[BGMSynthesizer] Saved {path}")
        else:
            print(f"[BGMSynthesizer] {filename} already exists, skipping.")

if __name__ == "__main__":
    generate_all_stock_bgm()
