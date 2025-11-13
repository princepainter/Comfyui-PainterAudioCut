<div align="center">

# ComfyUI Painter Audio Cut

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/Powered%20by-ComfyUI-orange)](https://github.com/comfyanonymous/ComfyUI)

</div>

<div align="center">
  <h3>English | 中文</h3>
</div>

---

## 🎯 简介 | Introduction

**本节点由抖音博主：绘画小子 制作。**
**ComfyUI Painter Audio Cut** 是一个基于帧率的高精度音频剪切自定义节点。  
**ComfyUI Painter Audio Cut** is a high-precision audio trimming custom node based on frame rates.

通过帧数而非时间戳实现音频的精确裁剪，完美适配视频帧同步需求。  
Trim audio precisely by frame numbers instead of timestamps, perfectly matching video frame synchronization needs.

---

## ✨ 核心特性 | Key Features

| 中文 | English |
|------|--------|
| 🎯 **帧级精度控制** - 按帧数裁剪，与视频帧率完美同步 | 🎯 **Frame-level Precision** - Trim by frame numbers, perfectly sync with video FPS |
| ⚡ **高性能处理** - 基于 PyTorch 张量操作，实时无延迟 | ⚡ **High Performance** - Real-time processing with PyTorch tensor operations |
| 🔒 **智能边界处理** - 自动处理越界，防止报错中断 | 🔒 **Smart Boundary Handling** - Auto-handle out-of-bounds to prevent errors |
| 🎵 **标准格式兼容** - 完全兼容 ComfyUI 音频格式 | 🎵 **Standard Format Compatible** - Fully compatible with ComfyUI audio format |
| 🛠️ **极简操作界面** - 三个参数，直观易用 | 🛠️ **Minimalist UI** - Three parameters, intuitive and easy to use |

---

## 📦 安装指南 | Installation

### 方法一：Git 克隆（推荐）| Method 1: Git Clone (Recommended)

```bash
# 进入 ComfyUI 自定义节点目录 | Navigate to ComfyUI custom nodes directory
cd ComfyUI/custom_nodes
```
# 克隆本仓库 | Clone this repository
git clone https://github.com/princepainter/Comfyui-PainterAudioCut.git
方法二：手动安装 | Method 2: Manual Installation
下载本仓库 ZIP 包 | Download the ZIP file of this repository
解压到 ComfyUI/custom_nodes/ 目录 | Extract to ComfyUI/custom_nodes/ directory
重启 ComfyUI | Restart ComfyUI
🔧 参数说明 | Parameters
参数	Type	Default	中文说明	English Description
audio	AUDIO	-	输入音频（需连接音频输出节点）	Input audio (connect from audio output node)
frame_rate	INT	30	每秒帧数（fps），决定时间分割精度	Frames per second, determines time division precision
start_frame	INT	0	包含的起始帧索引（从 0 开始）	Inclusive start frame index (0-based)
end_frame	INT	30	不包含的结束帧索引	Exclusive end frame index
📊 使用示例 | Usage Examples
示例 1 | Example 1: 裁剪前 1 秒 | Trim First Second
场景 | Scenario: 5 秒音频，删除前 1 秒

Audio: 5 seconds, remove first 1 second

python
编辑
# 参数设置 | Parameters
frame_rate  = 30     # 1秒 = 30帧 | 1 second = 30 frames
start_frame = 30     # 跳过30帧 = 1秒 | Skip 30 frames = 1 second
end_frame   = 150    # 5秒 × 30fps = 150帧 | 5s × 30fps = 150 frames

# 输出 | Output: 第30-149帧（1.0s ~ 5.0s）
# Result: Frames 30–149 (corresponding to 1.0s ~ 5.0s)
示例 2 | Example 2: 提取中间片段 | Extract Middle Section
场景 | Scenario: 提取第 2–4 秒音频

Audio: Extract audio from 2nd to 4th second

python
编辑
frame_rate  = 30
start_frame = 60     # 2 × 30 = 60帧 | 2 × 30 = 60 frames
end_frame   = 120    # 4 × 30 = 120帧 | 4 × 30 = 120 frames

# 输出 | Output: 第60-119帧（共60帧=2秒）
# Result: Frames 60–119 (total 60 frames = 2 seconds)
示例 3 | Example 3: 高帧率精确裁剪 | High FPS Precision
python
编辑
frame_rate  = 60     # 60fps提供更高精度 | 60fps for higher precision
start_frame = 45     # 0.75秒 | 0.75 second
end_frame   = 90     # 1.5秒 | 1.5 seconds

# 输出 | Output: 0.75s ~ 1.5s 片段
# Result: Audio clip from 0.75s to 1.5s
⚠️ 边界规则 | Boundary Rules
重要 | IMPORTANT: 本节点采用 Python 标准切片规则

This node uses Python standard slicing rules

起始帧 | Start Frame: 包含该帧数据 (INCLUSIVE)
结束帧 | End Frame: 不包含该帧数据 (EXCLUSIVE)
