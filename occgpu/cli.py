# occgpu/cli.py
import argparse
import os
from .core import scramble_gpus
from .utils import get_env_or, validate_proportion, validate_positive_int

def main():
    default_proportion = get_env_or(
        "OCCGPU_P",
        0.9,
        validate_proportion
    )
    default_gpu_nums = get_env_or(
        "OCCGPU_N",
        3,
        validate_positive_int
    )

    parser = argparse.ArgumentParser(
        description="Occupy free GPU memory to prevent others from using it."
    )
    parser.add_argument(
        '-p', '--proportion',
        type=validate_proportion,
        default=default_proportion,
        help='Min ratio of free/total GPU memory to target (0 < p ≤ 1). Env: $OCCGPU_PROPORTION'
    )
    parser.add_argument(
        '-n', '--gpu_nums',
        type=validate_positive_int,
        default=default_gpu_nums,
        help='Number of GPUs to occupy. Env: $OCCGPU_GPU_NUMS'
    )
    parser.add_argument(
        '-t', '--times',
        type=int,
        default=1800,
        help='Time to sleep after occupying (seconds)'
    )
    parser.add_argument(
        '-e', '--email_conf',
        type=str,
        default='./email_conf.json',
        help='Path to email config (not used currently)'
    )

    args = parser.parse_args()


    print("🚀 occgpu started with settings:")
    print(f"   - Proportion threshold (-p): {args.proportion:.2f}")
    print(f"   - Target GPU count (-n): {args.gpu_nums}")
    print(f"   - Sleep time after occupation (-t): {args.times} seconds")
    if os.getenv('OCCGPU_PROPORTION'):
        print(f"   🌐 (OCCGPU_PROPORTION={os.getenv('OCCGPU_PROPORTION')} used as default)")
    if os.getenv('OCCGPU_GPU_NUMS'):
        print(f"   🌐 (OCCGPU_GPU_NUMS={os.getenv('OCCGPU_GPU_NUMS')} used as default)")
    print("-" * 50)


    scramble_gpus(
        proportion=args.proportion,
        gpu_nums=args.gpu_nums,
        sleep_time=args.times
    )