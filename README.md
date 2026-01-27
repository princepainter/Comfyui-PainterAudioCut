# ComfyUI Audio Cut Node / ComfyUI 音频剪切节点

<img width="1390" height="483" alt="image" src="https://github.com/user-attachments/assets/5a41a731-8e5d-4654-8de2-6b2c323499cc" />


**English** |本节点由抖音博主：绘画小子 制作 [中文](#中文)

**PainterAudioCut**

专为视频生成设计的精准音频裁剪节点。按帧率定位裁剪点，自动对齐 4N+1 帧格式，支持头尾静音插入，完美匹配 Wan2.1 等模型的音频长度要求。

**参数说明**
- **frame_rate**: 视频帧率（如 30fps 视频填 30）
- **head_silence_frames**: 开头插入静音帧数（0-1000），用于对齐音频起始
- **start_frame**: 原音频裁剪起始帧（从 0 开始）
- **end_frame**: 原音频裁剪结束帧
- **tail_silence_frames**: 结尾追加静音帧数（0-1000）

**输出**
- **trimmed_audio**: 处理后的音频数据
- **total_frame**: 对齐后的总帧数（4N+1 格式）

**典型用法**
连接 Wan2.1 视频工作流，帧率与视频一致，通过头尾静音调节音频起始时间，节点自动确保输出长度符合模型要求（如 121、125 帧等）。

**PainterAudioCut**

A precision audio trimming node designed for video generation workflows. Cuts audio segments by frame-based timing and automatically aligns output to 4N+1 frame format (required by Wan2.1 and similar video models).

**Parameters**
- **frame_rate**: Target video frame rate (e.g., 30 for 30fps video)
- **head_silence_frames**: Silent frames to insert at the beginning (0-1000)
- **start_frame**: Cut start position in original audio (0-based)
- **end_frame**: Cut end position in original audio
- **tail_silence_frames**: Silent frames to append at the end (0-1000)

**Outputs**
- **trimmed_audio**: Processed audio tensor
- **total_frame**: Total aligned frame count (4N+1 format)

**Typical Usage**
Connect to Wan2.1 video generation workflows. Set `frame_rate` matching your video, define audio segment with `start_frame`/`end_frame`, and use `head_silence_frames` to sync audio start with video timing. The node ensures audio length automatically aligns to model requirements (e.g., 121, 125, 129 frames).
