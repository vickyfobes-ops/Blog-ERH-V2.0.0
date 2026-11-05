@echo off
setlocal
chcp 65001 >nul
where py >nul 2>nul
if not errorlevel 1 (
  set "ERH_PYTHON=py -3"
  goto ready
)
where python >nul 2>nul
if not errorlevel 1 (
  set "ERH_PYTHON=python"
  goto ready
)
echo Python not found. Open this folder in Codex and use the installation prompt.
pause
exit /b 1
:ready
%ERH_PYTHON% -X utf8 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 'Python 3.10+ required; ask Codex to use its bundled Python.')"
if errorlevel 1 goto failed
%ERH_PYTHON% -X utf8 "%~dp0verify_package.py"
if errorlevel 1 goto failed
%ERH_PYTHON% -X utf8 "%~dp0blog-erh-v2-0-0\scripts\install_local.py" --replace %*
if errorlevel 1 goto failed
echo Installation complete. Send your topic to Codex in the next message.
pause
exit /b 0
:failed
echo Installation failed. Send the error above to Codex.
pause
exit /b 1
