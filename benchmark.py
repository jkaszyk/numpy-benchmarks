import importlib
import argparse
import sys
import os.path
import glob
import timeit
import string
import shutil

blacklist = ['check_mask.py',
            'make_decision.py',
            'multiple_sum.py',
            'normalize_complex_arr.py',
            'slowparts.py',
            'wdist.py',
            'periodic_dist.py',
            'diffusion.py'
            ]

def runner_delayrepay(res):
    import delayrepay
    if isinstance(res, delayrepay.DelayArray):
        res.run() 
    delayrepay.cuda.Device().synchronize()

def runner_cupy(res):
    import cupy
    cupy.cuda.Device().synchronize()

def runner_numpy(res):
    pass

def eprint(*args):
    print(*args, file=sys.stderr)


posts = {"numpy": runner_numpy, "cupy": runner_cupy, "delayrepay":
    runner_delayrepay}
parser = argparse.ArgumentParser(description='runs your benchmarks')
parser.add_argument('--libs', default=['numpy,cupy,delayrepay'])
parser.add_argument('files', nargs = '+')
args = parser.parse_args()
libs = [importlib.import_module(name) for name in args.libs.split( ',')]

benchmarks = args.files

for benchmark in benchmarks:
    benchname = os.path.basename(benchmark)
    if benchname in blacklist and len(benchmarks) > 1:
        continue
    mod_path = benchmark[:-3].replace("/", ".")
    mod = importlib.import_module(mod_path)
    eprint(benchmark)
    for lib in libs:
        try:
            os.system('rm -fr ~/.nv/ComputeCache')
            os.system('rm -fr ~/.cupy/kernel_cache')
        except OSError as ex:
            eprint(ex)
        mod.np=lib
        mod.numpy=lib
        try:
            data = mod.data(lib)
            def runner():
                res = mod.func(lib, data)
                posts[lib.__name__](res)

            times = timeit.repeat(runner, repeat=10, number=1)
            print(f"{benchname}, {lib.__name__}, {','.join(map(str, times))}")
        except (ValueError, TypeError) as ex:
            eprint("probably unsupported by cupy")
            eprint(ex)
            print(f"{benchname}, {lib.__name__}, N/A")
            raise
