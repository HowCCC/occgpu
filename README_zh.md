
---

## 📄 `README_zh.md`（中文版）

```markdown
# occgpu：占用空闲 GPU 显存

**通过自动占用 GPU 空闲显存，防止他人使用。**  
非常适合实验室、高校服务器或共享云集群等多人共用 GPU 的环境。

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Unix-orange)

---

## 🚀 功能特性

- ✅ **自动检测空闲 GPU** – 使用 `nvidia-smi` 查找显存空闲较多的 GPU。
- ✅ **可配置阈值** – 仅占用“空闲显存 / 总显存 > 比例”的 GPU。
- ✅ **多 GPU 支持** – 可同时占用多个 GPU。
- ✅ **PyTorch & TensorFlow 自动回退** – 优先使用 PyTorch，失败时自动切换到 TensorFlow。
- ✅ **灵活配置** – 支持 **命令行参数** 和 **环境变量** 两种方式设置。
- ✅ **安全清理** – 支持 `Ctrl+C` 安全退出，自动终止占用进程。
- ✅ **轻量独立** – 除 `numpy` 外无其他强制依赖。

---

## 📦 使用方法

```bash
# 克隆项目
git clone https://github.com/howcca/occgpu.git
cd occgpu

pip install -e .

#配置环境变量
export OCCGPU_N = <NUMBERS>
export OCCGPU_P = <Proportion>

occgpu

#或者直接通过命令行传入

occgpu -p <Proportion> -n <NUMBERS>