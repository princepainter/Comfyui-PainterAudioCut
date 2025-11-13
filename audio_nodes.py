import torch
import numpy as np

class PainterAudioCut:
    """
  An audio trimming node for ComfyUI that cuts audio by setting start and end frames based on a specified frame rate.
  
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),  # 音频输入
                "frame_rate": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 120,
                    "step": 1,
                    "display": "number"
                }),  # 每秒帧数
                "start_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),  # 起始帧
                "end_frame": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),  # 结束帧
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("trimmed_audio",)
    FUNCTION = "trim_audio"
    CATEGORY = "audio/processing"
    
    def trim_audio(self, audio, frame_rate, start_frame, end_frame):
        """
        剪切音频的主要逻辑
        
        Args:
            audio: 输入音频字典，包含'waveform'和'sample_rate'
            frame_rate: 每秒多少帧
            start_frame: 起始帧
            end_frame: 结束帧
        
        Returns:
            剪切后的音频字典
        """
        # 验证输入
        if frame_rate <= 0:
            raise ValueError("帧率必须大于0")
        if start_frame >= end_frame:
            raise ValueError("起始帧必须小于结束帧")
        
        # 获取音频数据
        waveform = audio["waveform"]  # shape: (batch, channels, samples)
        sample_rate = audio["sample_rate"]
        
        # 计算每帧的样本数
        samples_per_frame = sample_rate / frame_rate
        
        # 计算起始和结束的样本位置
        start_sample = int(start_frame * samples_per_frame)
        end_sample = int(end_frame * samples_per_frame)
        
        # 确保不超出音频边界
        total_samples = waveform.shape[-1]
        start_sample = min(start_sample, total_samples)
        end_sample = min(end_sample, total_samples)
        
        # 切片音频
        trimmed_waveform = waveform[..., start_sample:end_sample]
        
        # 返回剪切后的音频
        return ({
            "waveform": trimmed_waveform,
            "sample_rate": sample_rate
        },)
    
    @classmethod
    def IS_CHANGED(cls, audio, frame_rate, start_frame, end_frame):
        """
        告诉ComfyUI何时需要重新执行节点
        """
        return float("NaN")

# 节点映射
NODE_CLASS_MAPPINGS = {
    "PainterAudioCut": PainterAudioCut
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PainterAudioCut": "Painter Audio Cut"
}

# Web目录（如果需要自定义前端）
WEB_DIRECTORY = "./web"
