@echo off
:: Batch file for building crlibm on AppVeyor

PATH C:\msys64\MINGW%PYTHON_ARCH%\bin;C:\msys64\usr\bin;%PATH%
bash -lc "make -C /c/projects/pyinterval/deps msys2"

@echo on
gendef %PYTHON_DLL%
dlltool --dllname %PYTHON_DLL% --def python27.def --output-lib deps\build\lib\libpython27.a

@echo off
%PYTHON%/python setup.py build_ext -i -c msys2 && echo Success. || echo Failed.
%PYTHON%/python -c "import crlibm"
