@echo off
echo ==============================
echo LingoLens v1.0 EXE Build
echo ==============================

cd /d C:\LingoLens

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller ^
 --noconfirm ^
 --onefile ^
 --windowed ^
 --name LingoLens ^
 --icon "assets\logo\LingoLens.ico" ^
 --add-data "assets;assets" ^
 --add-data "models;models" ^
 main.py

echo.
echo Build tamamlandi.
echo EXE burada:
echo C:\LingoLens\dist\LingoLens.exe
pause