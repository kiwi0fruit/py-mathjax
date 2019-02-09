# MathJax

MathJax in pip and conda.

# Install

Needs python 3.6+

```bash
conda install -c defaults -c conda-forge py-mathjax
```

or

```bash
pip install py-mathjax
```


# API

### mathjax_path

```py
def mathjax_path(as_url: bool=False) -> str:
    """ Returns MathJax.js file absolute path. """
```

### CLI

```
Usage: py-mathjax-path [OPTIONS]

  Prints MathJax.js file absolute path.

Options:
  --url, -u    print MathJax.js file abs path as URL,
  --help, -h   Show this message and exit.
```
