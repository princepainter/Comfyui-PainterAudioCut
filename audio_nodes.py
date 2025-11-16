import torch
import numpy as np

class PainterAudioCut:
    """
    An audio trimming node for ComfyUI that cuts audio by setting start and end frames based on a specified frame rate.
    Supports negative start_frame to add silence at the beginning.
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
                    "min": -999999,  # 允许负值以添加静音
                    "max": 999999,
                    "step": 1,
                    "display": "number"
                }),  # 起始帧，负数表示在前面添加静音
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
            start_frame: 起始帧，负数表示在音频前添加静音
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
        
        # 总样本数
        total_samples = waveform.shape[-1]
        
        if start_frame < 0:
            # 处理负数起始帧：在音频前添加静音
            silence_frames = abs(start_frame)
            silence_samples = int(silence_frames * samples_per_frame)
            
            # 确保结束样本位置不超出音频边界
            end_sample = min(int(end_frame * samples_per_frame), total_samples)
            
            # 创建静音片段（与原音频相同的形状和数据类型）
            # 形状: (batch, channels, silence_samples)
            silence_shape = list(waveform.shape)
            silence_shape[-1] = silence_samples
            silence_waveform = torch.zeros(*silence_shape, dtype=waveform.dtype, device=waveform.device)
            
            # 从原音频开头切片到结束位置
            audio_slice = waveform[..., 0:end_sample]
            
            # 拼接静音和音频
            trimmed_waveform = torch.cat([silence_waveform, audio_slice], dim=-1)
        else:
            # 正常处理正数起始帧
            start_sample = int(start_frame * samples_per_frame)
            end_sample = min(int(end_frame * samples_per_frame), total_samples)
            
            # 确保不超出音频边界
            start_sample = min(start_sample, total_samples)
            
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
