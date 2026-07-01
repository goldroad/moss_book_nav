$hookSrc = "C:\Python312\Lib\site-packages\cefpython3\examples\pyinstaller\hook-cefpython3.py"
$hookDst = "C:\Python312\Lib\site-packages\PyInstaller\hooks\hook-cefpython3.py"
Copy-Item -Path $hookSrc -Destination $hookDst -Force
Write-Output "hook copied to $hookDst"
