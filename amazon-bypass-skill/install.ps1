# install.ps1 - Installe Harbor Amazon v2 sur le PC Windows.
#
# Ce script fait trois choses seulement :
#   1. pip install des dependances en wheels, DIRECTEMENT dans
#      Lib\site-packages du Python portable (aucun venv, aucune
#      construction depuis les sources, aucun PYTHONPATH).
#   2. Copie du paquet harbor_amazon dans Lib\site-packages, puis
#      verification de l'import.
#   3. Verification que Chromium se lance (check_browser.py). Si les
#      navigateurs sont absents, un seul `playwright install chromium`,
#      puis on reteste une fois. Si ca echoue encore, STOP.
#
# V2 : Playwright remplace curl_cffi (la v1 se faisait servir un 503
# direct par Amazon en requete HTTP). Le navigateur Chromium est
# celui de C:\Users\muse-build\work\tools\ms-playwright.
#
# A lancer depuis le dossier src/ du skill :
#   cd C:\Users\muse-build\work\amazon-bypass-maison\src
#   .\install.ps1

$ErrorActionPreference = "Continue"
# Note : git et pip ecrivent leur progression sur stderr. Avec "Stop",
# PowerShell transformerait ces lignes en erreur fatale. On garde
# "Continue" et on verifie $LASTEXITCODE apres chaque commande externe.

$Python = "C:\Users\muse-build\work\tools\python-embed\python.exe"
$PythonDir = Split-Path -Parent $Python
$SitePackages = Join-Path $PythonDir "Lib\site-packages"
$PackageSource = Join-Path $PSScriptRoot "harbor_amazon"
$PackageTarget = Join-Path $SitePackages "harbor_amazon"
$BrowsersPath = "C:\Users\muse-build\work\tools\ms-playwright"

if (-not $env:PLAYWRIGHT_BROWSERS_PATH) {
    $env:PLAYWRIGHT_BROWSERS_PATH = $BrowsersPath
}

if (-not (Test-Path $Python)) {
    Write-Host "STOP : Python portable introuvable : $Python"
    exit 1
}
& $Python --version
if ($LASTEXITCODE -ne 0) { Write-Host "STOP : python --version a echoue"; exit 1 }

if (-not (Test-Path $PackageSource)) {
    Write-Host "STOP : paquet introuvable : $PackageSource"
    exit 1
}

Write-Host "Installation des dependances en wheels dans Lib\site-packages..."
& $Python -m pip install fastapi uvicorn pydantic beautifulsoup4 playwright 2>&1 | Out-Host
if ($LASTEXITCODE -ne 0) {
    Write-Host "STOP : pip install a echoue, code $LASTEXITCODE"
    exit 1
}

Write-Host "Copie du paquet harbor_amazon dans Lib\site-packages..."
if (Test-Path $PackageTarget) {
    Remove-Item -Recurse -Force $PackageTarget
}
Copy-Item -Recurse -Force $PackageSource $PackageTarget
# Note : Copy-Item est une cmdlet, $LASTEXITCODE ne s'applique pas.
# On verifie que le fichier principal est bien arrive.
if (-not (Test-Path (Join-Path $PackageTarget "__init__.py"))) {
    Write-Host "STOP : copie du paquet echouee"
    exit 1
}

Write-Host "Verification de l'import..."
& $Python -c "import harbor_amazon; print('harbor_amazon', harbor_amazon.__version__)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "STOP : import harbor_amazon echoue"
    exit 1
}

Write-Host "Verification du navigateur Chromium..."
& $Python (Join-Path $PSScriptRoot "check_browser.py")
if ($LASTEXITCODE -ne 0) {
    Write-Host "Chromium absent ou non demarrable, installation des navigateurs..."
    & $Python -m playwright install chromium 2>&1 | Out-Host
    if ($LASTEXITCODE -ne 0) {
        Write-Host "STOP : playwright install chromium a echoue, code $LASTEXITCODE"
        exit 1
    }
    & $Python (Join-Path $PSScriptRoot "check_browser.py")
    if ($LASTEXITCODE -ne 0) {
        Write-Host "STOP : Chromium ne demarre toujours pas apres installation"
        exit 1
    }
}

Write-Host "Installation OK."
