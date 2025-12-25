# ComfyUI Audio Cut Node / ComfyUI 音频剪切节点

**English** |本节点由抖音博主：绘画小子 制作 [中文](#中文)

---

## English

A simple audio trimming node for ComfyUI that supports adding silence by using negative start frame values.
![QQ截图20251225164419](https://github.com/user-attachments/assets/70e0a16f-4fd4-4531-a796-ec91cf45ffbc)

### Features

- Trim audio by frame numbers based on frame rate
- After the upgrade, it now supports audio frame count output.
- Add silence at the beginning using negative `start_frame` values
- Maintains original audio format and sample rate

### Installation

1. Clone or download this repository into your ComfyUI `custom_nodes` directory:
   ```
   ComfyUI/custom_nodes/ComfyUI-Audio-Cut/
   ```
2. Restart ComfyUI

### Usage

Add the **"Painter Audio Cut"** node from `audio/processing` category.

#### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `audio` | Input audio (expects `AUDIO` type from Load Audio node) | - |
| `frame_rate` | Frames per second for calculation | `30` |
| `start_frame` | Starting frame. **Negative values add silence** | `-30` |
| `end_frame` | Ending frame (audio will be trimmed here) | `1000` |

#### How Negative Start Frame Works

When `start_frame` is negative, the node adds silent frames **before** your audio:
- Silence duration = `abs(start_frame) / frame_rate` seconds
- The original audio starts playing after the silence
- Total output length = silence + trimmed audio portion

#### Examples

**Add 1 second of silence to 5-second audio:**
- Input: 5s audio (150 frames @ 30fps)
- Settings: `start_frame = -30`, `end_frame = 150`
- Output: 6s audio (1s silence + 5s original)

**Normal trimming (no silence):**
- Settings: `start_frame = 30`, `end_frame = 90`
- Output: Trims audio from 1s to 3s (60 frames @ 30fps)

#### Input/Output Format

**Input Audio Format:**
```python
{
  "waveform": torch.Tensor,  # shape: (batch, channels, samples)
  "sample_rate": int
}
```

**Output:** Same format as input, with trimmed/modified waveform

---

## 中文

ComfyUI 的简单音频剪切节点，支持使用负起始帧值来添加静音片段。本节点由抖音博主：绘画小子 制作

### 功能特点

- 基于帧率和帧号剪切音频
- 升级后，现在支持输出音频的帧数
- 使用负的 `start_frame` 值在音频开头添加静音
- 保持原始音频格式和采样率不变
![QQ截图20251225164419](https://github.com/user-attachments/assets/70e0a16f-4fd4-4531-a796-ec91cf45ffbc)
### 安装方法

1. 将本仓库克隆或下载到 ComfyUI 的 `custom_nodes` 目录：
   ```
   ComfyUI/custom_nodes/ComfyUI-Audio-Cut/
   ```
2. 重启 ComfyUI

### 使用说明

在 `audio/processing` 类别中添加 **"Painter Audio Cut"** 节点。

#### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `audio` | 输入音频（接收 Load Audio 节点的 `AUDIO` 类型） | - |
| `frame_rate` | 每秒帧数，用于计算 | `30` |
| `start_frame` | 起始帧。**负值表示添加静音** | `-30` |
| `end_frame` | 结束帧（音频将在此帧处截断） | `1000` |

#### 负起始帧的工作原理

当 `start_frame` 为负数时，节点会在音频前添加静音片段：
- 静音时长 = `abs(start_frame) / frame_rate` 秒
- 原始音频在静音结束后开始播放
- 总输出长度 = 静音时长 + 截取的音频部分

#### 使用示例

**为 5 秒音频添加 1 秒静音：**
- 输入：5 秒音频（150 帧 @ 30fps）
- 设置：`start_frame = -30`, `end_frame = 150`
- 输出：6 秒音频（1 秒静音 + 5 秒原音频）

**普通剪切（不添加静音）：**
- 设置：`start_frame = 30`, `end_frame = 90`
- 输出：从第 1 秒剪切到第 3 秒（60 帧 @ 30fps）

#### 输入输出格式

**输入音频格式：**
```python
{
  "waveform": torch.Tensor,  # 形状: (batch, channels, samples)
  "sample_rate": int
}
```

**输出：** 与输入格式相同，波形数据经过剪切或修改

---

### License / 许可证

MIT License - Feel free to use and modify. / MIT 许可证 - 可自由使用和修改。
