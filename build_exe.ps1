$ErrorActionPreference = "Stop"

Write-Host "== Text Merge Build (.exe) ==" -ForegroundColor Cyan

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    throw "Virtual environment not found at .\venv. Create it first."
}

$py = ".\venv\Scripts\python.exe"

Write-Host "Installing/Updating build dependencies..." -ForegroundColor Yellow
& $py -m pip install --upgrade pip | Out-Null
& $py -m pip install -r requirements.txt | Out-Null
& $py -m pip install pyinstaller | Out-Null

Write-Host "Cleaning old build artifacts..." -ForegroundColor Yellow
if (Test-Path ".\build") { Remove-Item ".\build" -Recurse -Force }
if (Test-Path ".\dist") { Remove-Item ".\dist" -Recurse -Force }

Write-Host "Building one-folder GUI app..." -ForegroundColor Yellow
& $py -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name "TextMergeApp" `
  --add-data "fonts;fonts" `
  --add-data "src;src" `
  --collect-all customtkinter `
  gui_launcher.py

Write-Host "Build completed: .\dist\TextMergeApp\" -ForegroundColor Green
