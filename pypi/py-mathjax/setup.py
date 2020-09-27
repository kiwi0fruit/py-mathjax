from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import io
import os.path as p
import platform
import shutil

src_dir = p.dirname(p.abspath(__file__))


def assert_64_bit_os():
    if not (platform.machine().endswith('64') or  # 64 bit OS if method is OK
            platform.architecture()[0] == '64bit'):  # 64 bit Python
        raise RuntimeError('Only 64bit OS is supported.')


def read_pythonic_config(file_path, vars_):
    import configparser
    from ast import literal_eval
    with io.open(file_path, 'r', encoding='utf-8') as f:
        config = configparser.ConfigParser()
        config.read_string('[_]\n' + f.read())
    return [literal_eval(config.get('_', var)) for var in vars_]


# ------------------------------------------------------------------------------
# Custom settings:
# ------------------------------------------------------------------------------
version, conda = [read_pythonic_config(p.join(src_dir, 'pymathjax', var + '.py'), [var])[0]
                  for var in ('version', 'conda')]
# assert_64_bit_os()
conda_version, build = version, '.1'  # was: version, '.4'
tmp = 'tmp'
spec = dict(
    Linux=dict(
        os='linux', move=[('lib/mathjax', tmp)], version=conda_version, build=0,
        hash_='a92311af0beaa0fea8cd9e77ea15ae09127b04199e94c180818bee7aa468a361'
    ),
)
spec = spec.get(platform.system(), spec['Linux'])
URL = 'https://anaconda.org/conda-forge/mathjax/{version}/download/{os}-64/mathjax-{version}-{build}.tar.bz2'.format(**spec)


class PostInstallCommand(install):
    def run(self):
        excract_tar_and_move_files(url=URL, **spec)
        move_contents(
            from_=p.join(src_dir, tmp),
            to=p.join(self.install_lib, 'pymathjax', 'mathjax'))
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


def excract_tar_and_move_files(url, hash_, move, **kwargs):
    """
    Moves relative to the setup.py dir. Can download more packages
    if the target archive contains setup.py

    * ``url`` should be of the form z/name.x.y.gz
      (gz, bz2 or other suffix supported by the tarfile module).
    * ``move`` contains pairs of dirs where to move contents.
      First dir is in the extracted archive,
      second dir is in the same folder as setup.py
      WARNING: Mind that the second dir would be cleaned!
    """
    import sys
    from subprocess import run, PIPE
    import tempfile
    import tarfile

    cwd = os.getcwd()
    dirpath = tempfile.mkdtemp()
    try:
        os.chdir(dirpath)

        temp_dir = p.join(os.getcwd(), '__temp__')
        os.makedirs(temp_dir, exist_ok=True)
        req_path = p.join(os.getcwd(), 'requirements.txt')
        req_text = '{url} --hash=sha256:{hash_}\n'.format(url=url, hash_=hash_)
        print(req_text, file=open(req_path, 'w', encoding='utf-8'))

        proc = run([sys.executable, "-m", "pip", "download", "--require-hashes", "-b", temp_dir, "--no-clean", "-r", req_path],
                   stdout=PIPE, stderr=PIPE, encoding='utf-8', env={**dict(os.environ), **dict(TMPDIR=temp_dir, TEMP=temp_dir)})

        if proc.stderr is None:
            raise AssertionError('pip download behaviour changed. Downgrade pip or wait for bugfix.\n' + 'assert proc.stderr is not None')
        stderr = str(proc.stderr)
        if not (('FileNotFoundError' in stderr) and ('setup.py' in stderr)):
            raise AssertionError('pip download behaviour changed. Downgrade pip or wait for bugfix.\n' + stderr)
        pip_tmp_dirs = os.listdir(temp_dir)
        if len(pip_tmp_dirs) != 1:
            raise AssertionError('pip download behaviour changed. Downgrade pip or wait for bugfix.\n' + 'assert len(pip_tmp_dirs) == 1')

        if 'sha256' in stderr.lower():
            raise AssertionError(stderr)
        pip_tmp_dir = p.join(temp_dir, pip_tmp_dirs[0])

        for _, to in move:
            to = p.normpath(p.join(src_dir, to))
            if p.isdir(to):
                shutil.rmtree(to)
        for from_, to in move:
            from_ = p.join(pip_tmp_dir, p.normpath(from_))
            to = p.normpath(p.join(src_dir, to))
            os.makedirs(to, exist_ok=True)
            for s in os.listdir(from_):
                to_s = p.join(to, s)
                shutil.move(p.join(from_, s), to_s if p.isfile(to_s) else to)
    except Exception as e:
        os.chdir(cwd)
        shutil.rmtree(dirpath)
        raise e
    os.chdir(cwd)
    shutil.rmtree(dirpath)


# ------------------------------------------------------------------------------
# Custom settings:
# ------------------------------------------------------------------------------
with io.open(p.join(src_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

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
