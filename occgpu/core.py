# occgpu/core.py
#Some code was stolen from https://github.com/wilmerwang/GPUSnatcher
import os
import time
import numpy as np
import multiprocessing

try:
    import torch
except ImportError:
    try:
        import tensorflow as tf
    except ImportError:
        print("No pytorch and tensorflow module, please install one of these!")
        raise ImportError("No deep learning framework found")

def query_gpu():
    qargs = ['index', 'memory.free', 'memory.total']
    cmd = 'nvidia-smi --query-gpu={} --format=csv,noheader'.format(','.join(qargs))
    results = os.popen(cmd).readlines()
    if not results:
        return np.array([]), ""

    result_np = []
    for line in results[1:]:
        result_np.append([''.join(filter(str.isdigit, word)) for word in line.split(',')])
    result_np = np.array(result_np).astype(int)
    header = results[0].strip()
    return result_np, header


class GPUManager:
    def __init__(self, proportion):
        self.proportion = proportion

    def choose_free_gpu(self):
        qresult, _ = query_gpu()
        if qresult.shape[0] == 0:
            print("No GPU found. Check nvidia-smi.")
            return [], []

        sorted_indices = np.argsort(-qresult[:, 1])
        selected = [i for i in sorted_indices if qresult[i][1] / qresult[i][2] > self.proportion]

        gpus_index = qresult[selected, 0]
        gpus_memory = qresult[selected, 1]
        return gpus_index, gpus_memory


def compute_storage_size(memory_mb):
    return int((memory_mb * 1024 * 1024 / 8) ** (1/3) * 0.9)


def worker(gpu_id, size):
    try:
        a = torch.zeros([size, size, size], dtype=torch.double, device=f'cuda:{gpu_id}')
        print(f"GPU {gpu_id}: Allocated torch tensor of size {size}^3")
        while True:
            torch.mul(a[0], a[0])
    except Exception as e:
        print(f"GPU {gpu_id}: PyTorch failed ({e}), falling back to TensorFlow")
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        a = tf.zeros([size, size, size], dtype=tf.dtypes.float64)
        print(f"GPU {gpu_id}: Allocated TensorFlow tensor of size {size}^3")
        while True:
            tf.matmul(a[0], a[0])


def scramble_gpus(proportion=0.9, gpu_nums=3, sleep_time=1800):
    gpu_manager = GPUManager(proportion=proportion)
    processes = []
    taken_gpus = []

    try:
        while True:
            free_gpus, free_memory = gpu_manager.choose_free_gpu()
            need_more = gpu_nums - len(processes)

            if need_more > 0 and len(free_gpus) > 0:
                for gpu_id, mem in zip(free_gpus[:need_more], free_memory[:need_more]):
                    size = compute_storage_size(mem)
                    p = multiprocessing.Process(target=worker, args=(gpu_id, size))
                    p.start()
                    processes.append(p)
                    taken_gpus.append(gpu_id)
                    print(f"✅ Scrambled GPU {gpu_id} with {mem} MB free memory")
                    time.sleep(5)  

            if len(taken_gpus) >= gpu_nums:
                print(f"🎯 All {gpu_nums} GPUs scrambled. Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                break

            time.sleep(60)  

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🧹 Cleaning up processes...")
        for p in processes:
            if p.is_alive():
                p.terminate()
        for p in processes:
            p.join()
        print("👋 Done.")