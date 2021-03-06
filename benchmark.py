import importlib
import argparse
import sys
import os.path
import glob
import timeit
import string

def runner_delayrepay(res):
    res.run()
    cupy.cuda.Device().synchronize()

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
    for lib in libs:
        benchname = os.path.basename(benchmark)
        mod_path = benchmark[:-3].replace("/", ".")
        mod = importlib.import_module(mod_path)
        mod.np=lib
        mod.numpy=lib
        try:
            data = mod.data(lib)
            def runner():
                res = mod.func(lib, data)
                posts[lib.__name__](res)

            times = timeit.repeat(runner, repeat=1, number=1)
            print(f"{benchname}, {lib.__name__}, {','.join(map(str, times))}")
        except (NameError, AttributeError) as ex:
            eprint("Non conforming")
            eprint(ex)
            print(f"{benchname}, {lib.__name__}, N/A")
        except (ValueError, TypeError) as ex:
            eprint("probably unsupported by cupy")
            eprint(ex)
            print(f"{benchname}, {lib.__name__}, N/A")
