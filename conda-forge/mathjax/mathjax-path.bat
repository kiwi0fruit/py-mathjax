@echo off
REM script_dir == [env_root]\Scripts\
set "script_dir=%~dp0"
set "mathjax=%script_dir:~0,-9%\Library\lib\mathjax\MathJax.js"
if exist "%mathjax%" (
    echo %mathjax%
) else (
    echo Error: "%mathjax%" was not found. 1>&2
)
