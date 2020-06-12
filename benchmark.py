import importlib
import sys
import os.path
import glob
import timeit

import numpy
import cupy

libs = [numpy, cupy, ]

def runner_delayrepay(res):
    res.run()
    cupy.cuda.Device().synchronize()

def runner_cupy(res):
    cupy.cuda.Device().synchronize()

def runner_numpy(res):
    pass


posts = {"numpy": runner_numpy, "cupy": runner_cupy, "delayrepay":
    runner_delayrepay}
benchmarks = glob.glob("benchmarks/*.py")

for benchmark in benchmarks:
    for lib in libs:
        benchname = os.path.basename(benchmark)
        mod_path = benchmark[:-3].replace("/", ".")
        mod = importlib.import_module(mod_path)
        import numpy as np
        try:
            data = mod.data(np)
            def runner():
                res = mod.func(np, *data)
                posts[lib.__name__](res)

            times = timeit.repeat(runner, repeat=1, number=1)
            print(f"{benchname}, {lib.__name__}, {','.join(map(str, times))}")
        except (NameError, AttributeError) as ex:
            print("Non conforming", file=sys.stderr)
            print(f"{benchname}, {lib.__name__}, N/A")
