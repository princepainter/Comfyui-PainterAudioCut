import torch
import numpy as np

class PainterAudioCut:
    """
    An audio trimming node for ComfyUI that cuts audio by setting start and end frames based on a specified frame rate.
    Supports negative start_frame to add silence at the beginning.
    Adds tail silence frames at the end of audio.
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
                "start_frame": ("INT", {
                    "default": 0,
                    "min": -999999,
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
    RETURN_NAMES = ("trimmed_audio", "total_frames")
    FUNCTION = "trim_audio"
    CATEGORY = "audio/processing"
    
    def trim_audio(self, audio, frame_rate, start_frame, end_frame, tail_silence_frames):
        """
        Main logic for trimming audio and adding tail silence
        
        Args:
            audio: Input audio dictionary containing 'waveform' and 'sample_rate'
            frame_rate: Frames per second (float)
            start_frame: Start frame, negative values add silence at beginning
            end_frame: End frame
            tail_silence_frames: Number of silence frames to add at the end
        
        Returns:
            Trimmed audio dictionary with tail silence and total frame count
        """
        # Validate inputs
        if frame_rate <= 0:
            raise ValueError("Frame rate must be greater than 0")
        if start_frame >= end_frame:
            raise ValueError("Start frame must be less than end frame")
        
        # Get audio data
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        
        # Calculate samples per frame
        samples_per_frame = sample_rate / frame_rate
        
        # Total samples
        total_samples = waveform.shape[-1]
        
        if start_frame < 0:
            # Handle negative start frame: add silence before audio
            silence_frames = abs(start_frame)
            silence_samples = int(silence_frames * samples_per_frame)
            end_sample = min(int(end_frame * samples_per_frame), total_samples)
            
            silence_shape = list(waveform.shape)
            silence_shape[-1] = silence_samples
            silence_waveform = torch.zeros(*silence_shape, dtype=waveform.dtype, device=waveform.device)
            
            audio_slice = waveform[..., 0:end_sample]
            trimmed_waveform = torch.cat([silence_waveform, audio_slice], dim=-1)
        else:
            # Normal processing for positive start frame
            start_sample = int(start_frame * samples_per_frame)
            end_sample = min(int(end_frame * samples_per_frame), total_samples)
            start_sample = min(start_sample, total_samples)
            trimmed_waveform = waveform[..., start_sample:end_sample]
        
        # Add tail silence if specified
        if tail_silence_frames > 0:
            tail_silence_samples = int(tail_silence_frames * samples_per_frame)
            silence_shape = list(trimmed_waveform.shape)
            silence_shape[-1] = tail_silence_samples
            tail_silence_waveform = torch.zeros(*silence_shape, dtype=trimmed_waveform.dtype, device=trimmed_waveform.device)
            trimmed_waveform = torch.cat([trimmed_waveform, tail_silence_waveform], dim=-1)
        
        # Calculate total frames for output audio
        total_output_samples = trimmed_waveform.shape[-1]
        total_frames = int(total_output_samples / samples_per_frame)
        
        return ({
            "waveform": trimmed_waveform,
            "sample_rate": sample_rate
        }, total_frames)
    
    @classmethod
    def IS_CHANGED(cls, audio, frame_rate, start_frame, end_frame, tail_silence_frames):
        """
        Tell ComfyUI when to re-execute the node
        """
        return float("NaN")

NODE_CLASS_MAPPINGS = {
    "PainterAudioCut": PainterAudioCut
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PainterAudioCut": "Painter Audio Cut"
}

WEB_DIRECTORY = "./web"
