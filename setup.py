import sys, os, glob, shutil
import setuptools

from setuptools import setup
from setuptools.command.install import install

class my_install(install):
    def run(self):
        install.run(self)
        #self.post_install()

    def post_install(self):
        xtl = self.download_src("https://github.com/QuantStack/xtl/archive/0.6.7.zip")
        self.cmake(xtl)

        xsimd = self.download_src("https://github.com/QuantStack/xsimd/archive/7.2.6.zip")
        self.cmake(xsimd)

        xtensor = self.download_src("https://github.com/QuantStack/xtensor/archive/0.20.10.zip")
        self.cmake(xtensor)

        pybind11 = self.download_src("https://github.com/pybind/pybind11/archive/v2.3.0.zip")
        self.cmake(pybind11,
                  '-DPYTHON_EXECUTABLE={}'.format(sys.executable))

        xpython = self.download_src("https://github.com/QuantStack/xtensor-python/archive/0.23.1.zip")
        self.cmake(xpython,
                  '-DPYTHON_EXECUTABLE={}'.format(sys.executable))

        xblas = self.download_src("https://github.com/QuantStack/xtensor-blas/archive/0.16.1.zip")
        self.cmake(xblas)

    def download_src(self, url):
        from io import BytesIO
        from zipfile import ZipFile
        from urllib.request import urlopen
        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        target_dir = os.path.join(self.prefix, "tmp", "download")
        zipfile.extractall(target_dir)
        return os.path.join(target_dir,
                            zipfile.namelist()[0]).rstrip(os.path.sep)

    def cmake(self, target, *args):
        import subprocess
        CMAKE_BIN_DIR = subprocess.check_output(
            [sys.executable,
             '-c',
             'from cmake import CMAKE_BIN_DIR; print(CMAKE_BIN_DIR)'])
        btarget = os.path.basename(target)
        CMAKE_BIN_DIR = CMAKE_BIN_DIR.decode().strip()
        cmake = os.path.join(CMAKE_BIN_DIR, "cmake")
        build_dir = os.path.join(self.prefix, "tmp", "build", btarget)
        os.makedirs(build_dir, exist_ok=True)
        subprocess.check_call([cmake, os.path.join("..", "..", "download",
                                                     btarget),
                               "-DCMAKE_INSTALL_PREFIX={}".format(self.prefix),
                               *args],
                              cwd=build_dir)
        subprocess.check_call([cmake, "--build", "."], cwd=build_dir)
        subprocess.check_call([cmake, "--build", ".", "--target", "install"], cwd=build_dir)


setup(
    name='numpy_benchmarks',
    version='0.1.0',
    description='A collection of numpy kernels for benchmarking',
    author='serge-sans-paille',
    author_email='serge.guelton@telecom-bretagne.eu',
    url='https://github.com/serge-sans-paille/numpy-benchmarks',
    license="BSD 3-Clause",
    install_requires=open('requirements.txt').read().splitlines(),
    packages=['numpy_benchmarks', 'numpy_benchmarks/benchmarks'],
    scripts=['numpy_benchmarks/np-bench'],
    cmdclass=dict(install=my_install),
)
