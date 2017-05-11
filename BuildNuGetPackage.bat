@echo off
REM Note that using -u is critical to have output appear properly ordered!
python -u %PF%/BuildNuGetPackage.py %1 %2