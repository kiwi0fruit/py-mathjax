from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import io
import os.path as p
import shutil


def read_pythonic_config(file_path, vars):
    import configparser
    from ast import literal_eval
    with io.open(file_path, 'r', encoding='utf-8') as f:
        config = configparser.ConfigParser()
        config.read_string('[_]\n' + f.read())
    return [literal_eval(config.get('_', var)) for var in vars]


src_dir = p.dirname(p.abspath(__file__))
version, conda = [read_pythonic_config(p.join(src_dir, 'pymathjax', var + '.py'), [var])[0]
                  for var in ('version', 'conda')]

with io.open(p.join(src_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# ------------------------------------------------------------------------------
# Custom settings:
# ------------------------------------------------------------------------------
build = '.2'
tmp = 'tmp'
spec = dict(
    move=[('lib/mathjax', tmp)], version=version, build=1,
    hash='a4157bfa03dd56531a6c7c58d1f0f127a283851b35b20e975b844dd52750e704'
)
URL = 'https://anaconda.org/conda-forge/mathjax/{version}/download/linux-64/mathjax-{version}-{build}.tar.bz2'.format(**spec)


class PostInstallCommand(install):
    def run(self):
        excract_tar_and_move_files(url=URL, **spec)
        move_contents(
            from_=p.join(src_dir, tmp),
            to=p.join(self.install_lib, 'pymathjax', 'mathjax-' + version))
        install.run(self)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def move_contents(from_, to, set_exec=False):
    import stat
    os.makedirs(to, exist_ok=True)
    for file in os.listdir(from_):
        to_file = p.join(to, file)
        shutil.move(p.join(from_, file),
                    to_file if p.isfile(to_file) else to)
        if p.isfile(to_file) and set_exec:
            if os.name != 'nt':
                st = os.stat(to_file)
                os.chmod(to_file, st.st_mode | stat.S_IEXEC)


def sha256(filename):
    """ https://stackoverflow.com/a/44873382/9071377 """
    import hashlib
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def excract_tar_and_move_files(url, hash, move, **kwargs):
    """
    Moves relative to the setup.py dir. Can download more packages
    if the target archive contains setup.py

    * ``url`` should be of the form z/name.x.y.gz
      (gz, bz2 or other suffix supported by the tarfile module).
    * ``move`` contains pairs of dirs where to move contents.
      First dir is in the extracted archive,
      second dir is in the same folder as setup.py
    """
    import sys
    import tarfile
    from subprocess import call, run, PIPE
    import tempfile

    dirpath = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(dirpath)

    call([sys.executable, "-m", "pip", "download", url], stdout=PIPE, stderr=PIPE)
    filename = url.split('/')[-1]
    ext = p.splitext(filename)[1][1:]
    if sha256(filename) != hash:
        raise RuntimeError(f'SHA256 hash does not match for {filename}')
    with tarfile.open(filename, f"r:{ext}") as tar:
        tar.extractall()

    for from_, to in move:
        from_ = p.abspath(p.normpath(from_))
        to = p.normpath(p.join(src_dir, to))
        os.makedirs(to, exist_ok=True)
        for s in os.listdir(from_):
            shutil.move(p.join(from_, s), to)
    os.chdir(cwd)
    shutil.rmtree(dirpath)


setup(
    name='py-mathjax',
    version=version + build,
    python_requires='>=3.6',
    description='Installs mathjax conda package in pip and conda.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kiwi0fruit/py-mathjax',
    author='kiwi0fruit',
    author_email='peter.zagubisalo@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'py-mathjax-path=pymathjax.__main__:cli',
        ],
    },
    **(dict(
        cmdclass={'install': PostInstallCommand}
    ) if not conda else {})
)
