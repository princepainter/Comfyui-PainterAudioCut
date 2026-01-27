import torch
import numpy as np

class PainterAudioCut:
    """
    An audio trimming node for ComfyUI that cuts audio by setting start and end frames based on a specified frame rate.
    Supports head silence frames at the beginning and tail silence frames at the end.
    Automatically aligns output frame count to 4N+1 format.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "frame_rate": ("FLOAT", {
                    "default": 30.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "head_silence_frames": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
                "start_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),
                "end_frame": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),
                "tail_silence_frames": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO", "INT")
    RETURN_NAMES = ("trimmed_audio", "total_frame")
    FUNCTION = "trim_audio"
    CATEGORY = "audio/processing"
    
    def trim_audio(self, audio, frame_rate, head_silence_frames, start_frame, end_frame, tail_silence_frames):
        if frame_rate <= 0:
            raise ValueError("Frame rate must be greater than 0")
        if start_frame >= end_frame:
            raise ValueError("Start frame must be less than end frame")
        
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        samples_per_frame = sample_rate / frame_rate
        total_samples = waveform.shape[-1]
        
        result_frames = []
        
        if head_silence_frames > 0:
            head_samples = int(head_silence_frames * samples_per_frame)
            head_shape = list(waveform.shape)
            head_shape[-1] = head_samples
            head_silence = torch.zeros(*head_shape, dtype=waveform.dtype, device=waveform.device)
            result_frames.append(head_silence)
        
        start_sample = int(start_frame * samples_per_frame)
        end_sample = min(int(end_frame * samples_per_frame), total_samples)
        start_sample = min(start_sample, total_samples)
        audio_slice = waveform[..., start_sample:end_sample]
        result_frames.append(audio_slice)
        
        if tail_silence_frames > 0:
            tail_samples = int(tail_silence_frames * samples_per_frame)
            tail_shape = list(waveform.shape)
            tail_shape[-1] = tail_samples
            tail_silence = torch.zeros(*tail_shape, dtype=waveform.dtype, device=waveform.device)
            result_frames.append(tail_silence)
        
        if len(result_frames) > 1:
            trimmed_waveform = torch.cat(result_frames, dim=-1)
        else:
            trimmed_waveform = result_frames[0]
        
        total_output_samples = trimmed_waveform.shape[-1]
        total_frames = int(total_output_samples / samples_per_frame)
        
        remainder = (total_frames - 1) % 4
        if remainder == 0:
            aligned_frames = total_frames
        else:
            aligned_frames = total_frames + (4 - remainder)
        
        target_samples = int(aligned_frames * samples_per_frame)
        current_samples = trimmed_waveform.shape[-1]
        
        if target_samples > current_samples:
            silence_samples = target_samples - current_samples
            silence_shape = list(trimmed_waveform.shape)
            silence_shape[-1] = silence_samples
            silence_waveform = torch.zeros(*silence_shape, dtype=trimmed_waveform.dtype, device=trimmed_waveform.device)
            final_waveform = torch.cat([trimmed_waveform, silence_waveform], dim=-1)
        else:
            final_waveform = trimmed_waveform[..., :target_samples]
        
        return ({"waveform": final_waveform, "sample_rate": sample_rate}, aligned_frames)
    
    @classmethod
    def IS_CHANGED(cls, audio, frame_rate, head_silence_frames, start_frame, end_frame, tail_silence_frames):
        return float("NaN")
