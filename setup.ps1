$ErrorActionPreference = 'Stop'
$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootPath

if (-not (Test-Path '.venv\Scripts\python.exe')) {
  python -m venv .venv
}
& '.venv\Scripts\python.exe' -m pip install --upgrade pip
& '.venv\Scripts\python.exe' -m pip install -r 'backend\requirements.txt'
npm install
npm --prefix frontend install
npm --prefix frontend install-scripts approve esbuild
if (-not (Test-Path 'backend\.env')) {
  Copy-Item 'backend\.env.example' 'backend\.env'
}
Write-Host ''
Write-Host 'Setup complete. Run .\run.ps1 to start the web app and API.' -ForegroundColor Green
