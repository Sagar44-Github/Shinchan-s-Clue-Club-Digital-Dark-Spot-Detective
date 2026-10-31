$ErrorActionPreference = 'Stop'
$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootPath
if (-not (Test-Path '.venv\Scripts\python.exe')) {
  throw 'Python environment is missing. Run .\setup.ps1 first.'
}
npm run dev
