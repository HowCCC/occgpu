# occgpu: Occupy Free GPU Memory

**Prevent others from using idle GPUs by automatically occupying their free memory.**  
Perfect for researchers or engineers who want to reserve GPU resources in shared environments (e.g., lab servers, cloud clusters).


---

## 🚀 Features

- ✅ **Auto-detect free GPUs** – Uses `nvidia-smi` to find GPUs with high free memory.
- ✅ **Configurable threshold** – Only target GPUs where `free_memory / total_memory > proportion`.
- ✅ **Multi-GPU support** – Can occupy multiple GPUs simultaneously.
- ✅ **Framework fallback** – Supports both **PyTorch** and **TensorFlow** (falls back if one is missing).
- ✅ **Command-line & environment variables** – Flexible configuration via CLI or `$OCCGPU_PROPORTION`, `$OCCGPU_GPU_NUMS`.
- ✅ **Safe cleanup** – Gracefully terminates processes on exit (`Ctrl+C` supported).
- ✅ **Lightweight & standalone** – No database or external services required.

---

## 📦 Installation & Usage

```bash

# Install from PyPi

occgpu is released on PyPi
https://pypi.org/project/occgpu/0.1.0/


pip install occgpu==0.1.0

# Clone the repo
git clone https://github.com/howccc/occgpu.git
cd occgpu

# Install in development mode
pip install -e .

# Environment Variable Configuration
export OCCGPU_N = <NUMBERS>
export OCCGPU_P = <Proportion>

occgpu

# or configure through the CLI(priorest)

occgpu -p <PROPORTION> -n <NUMBERS>


