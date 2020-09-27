import os.path as p
import sys
from .conda import conda


class PyMathJaxError(Exception):
    pass


def mathjax_path(as_url: bool=False) -> str:
    """ Returns MathJax.js file absolute path. """
    if conda:
        import os
        pyexedir = p.dirname(p.abspath(sys.executable))
        if os.name == 'nt':
            mathjax_dir = p.join(pyexedir, 'Library', 'lib', 'mathjax')
        else:
            mathjax_dir = p.join(p.dirname(pyexedir), 'lib', 'mathjax')
    else:
        mathjax_dir = p.join(p.dirname(p.abspath(__file__)), 'mathjax')
    mathjax = p.join(mathjax_dir, 'MathJax.js')
    if not p.isfile(mathjax):
        raise PyMathJaxError(f"'{mathjax}' wasn't found.")
    if as_url:
        import pathlib
        return pathlib.Path(mathjax).as_uri()
    else:
        return mathjax


def cli():
    """
    Usage: py-mathjax-path [OPTIONS]

      Prints MathJax.js file absolute path.

    Options:
      --url, -u    print MathJax.js file abs path as URL,
      --help, -h   Show this message and exit.
    """
    url = False
    if len(sys.argv) > 1:
        if sys.argv[1] in ('--url', '-u'):
            url = True
        elif sys.argv[1] in ('--help', '-u'):
            print(str(cli.__doc__).replace('\n    ', '\n'))
            return None
    sys.stdout.write(mathjax_path(as_url=url))


if __name__ == '__main__':
    cli()
