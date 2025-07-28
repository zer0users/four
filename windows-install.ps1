Write-Output "Warning! This installation is not tested, it's in deveploment, because four is for linux, if you are sure and you know what you are installing, Press enter to continue, please, But remember! God is with you!"
Read-Host "Enter to install"
$url = 'https://raw.githubusercontent.com/zer0users/four/refs/heads/main/build/four-windows.py'
$installDir = 'C:\Program Files\Four'
if (-not (Test-Path $installDir)) { New-Item -ItemType Directory -Path $installDir -Force }
$outputPy = Join-Path $installDir 'four.py'
Invoke-WebRequest -Uri $url -OutFile $outputPy
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python -or $python.Version.Major -lt 3) {
  $installer = "$env:TEMP\python-installer.exe"
  Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe' -OutFile $installer
  Start-Process -FilePath $installer -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait -Verb RunAs
}
$bat = Join-Path $installDir 'four.bat'
Set-Content -Path $bat -Encoding ASCII -Value '@echo off\r\npython "%~dp0four.py" %*'
$machinePath = [Environment]::GetEnvironmentVariable('Path','Machine')
if ($machinePath -notlike "*$installDir*") {
  $newPath = "$machinePath;$installDir"
  [Environment]::SetEnvironmentVariable('Path',$newPath,'Machine')
}
