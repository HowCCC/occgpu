# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse
import random
import multiprocessing
import json
import socket

import numpy as np
try:
    import torch
except ImportError:
    try:
        import tensorflow as tf
    except ImportError:
        print("No pytorch and tensorflow module, please install one of these!")
        sys.exit()

def set_parser():
    parser = argparse.ArgumentParser(description='Scramble free GPU memory to prevent others from using it.')
    parser.add_argument('-p', '--proportion', type=float, default=0.9,
                        help='The ratio of gpu free memory to total memory')
    parser.add_argument('-n', '--gpu_nums', type=int, default=3,
                        help='The numbers of GPU to scramble')
    parser.add_argument('-t', '--times', type=int, default=1800,
                        help='Sleep time if scramble gpu')
    parser.add_argument('-e', '--email_conf', type=str, default='./email_conf.json',
                        help='The path to email config')
    return parser.parse_args()


def parse(qargs, results):
    result_np = []
    for line in results[1:]:
        result_np.append([''.join(filter(str.isdigit, word)) for word in line.split(',')])
    result_np = np.array(result_np)
    return result_np


def query_gpu():
    qargs = ['index', 'memory.free', 'memory.total']
    cmd = 'nvidia-smi --query-gpu={} --format=csv,noheader'.format(','.join(qargs))
    results = os.popen(cmd).readlines()
    return parse(qargs, results), results[0].strip()


class GPUManager(object):
    def __init__(self, args):
        self._args = args

    def choose_free_gpu(self):
        qresult, qindex = query_gpu()
        qresult = qresult.astype('int')

        if qresult.shape[0] == 0:
            print('No GPU, Check it.')
            return [], []
        else:
            qresult_sort_index = np.argsort(-qresult[:, 1])
            idex = [i for i in qresult_sort_index if qresult[i][1]/qresult[i][2] > self._args.proportion]
            gpus_index = qresult[:, 0][idex]
            gpus_memory = qresult[:, 1][idex]
            return gpus_index, gpus_memory


def compute_storage_size(memory):
    return int(pow(memory * 1024 * 1024 / 8, 1/3) * 0.9)  


def worker(gpus_id, size):
    try:
        a = torch.zeros([size, size, size], dtype=torch.double, device=gpus_id)
        while True:
            torch.mul(a[0], a[0])
    except Exception:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpus_id)
        a = tf.zeros([size, size, size], dtype=tf.dtypes.float64)
        while True:
            tf.matmul(a[0], a[0])


def main(args, ids):
    gpu_manager = GPUManager(args)
    processes = []
    
    try:
        while True:
            gpus_free, gpus_memory = gpu_manager.choose_free_gpu()

            if len(gpus_free) == 0:
                pass
            else:
                sca_nums = args.gpu_nums - len(processes)
                if sca_nums > 0:
                    sizes = [compute_storage_size(i) for i in gpus_memory]
                    for gpus_id, size in zip(gpus_free[:sca_nums], sizes[:sca_nums]):
                        ids.append(gpus_id)
                        print("Scramble GPU {}".format(gpus_id))
                        p = multiprocessing.Process(target=worker, args=(gpus_id, size))
                        p.start()
                        processes.append(p)
                        time.sleep(5)
                
            if len(ids) >= args.gpu_nums:
                time.sleep(args.times)
                break
            time.sleep(60)

    except Exception as e:
        print(e)

    finally:
        for p in processes:
            if p.is_alive():
                p.terminate()
        for p in processes:
            p.join()


def cli():
    ids = []
    args = set_parser()
    main(args, ids)


if __name__ == '__main__':
    cli()