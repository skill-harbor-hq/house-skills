# start.ps1 - Demarre le serveur Harbor Amazon v2 sur le PC Windows.
#
# - Fixe PLAYWRIGHT_BROWSERS_PATH vers le dossier des navigateurs du
#   PC (la variable n'est pas persistante, il faut la fixer a chaque
#   demarrage, sinon Playwright ne trouve pas Chromium).
# - Genere la cle API locale si elle est absente (fichier api-key dans
#   le dossier du skill, longueur seulement dans les logs, jamais la
#   valeur).
# - Demarre le serveur lie a 127.0.0.1:8792 seulement, avec deux
#   journaux separes (server.log et server-err.log, car Start-Process
#   refuse stdout et stderr vers le meme fichier).
# - Attend /health 200 pendant 20 secondes maximum. Sinon, arrete le
#   serveur et affiche l'erreur exacte.
# - En cas de succes, le serveur reste en marche et le script se termine.
# - Le navigateur Chromium demarre paresseusement, a la premiere
#   requete Amazon : /health reste rapide. Si Chromium ne demarre pas,
#   l'API renvoie 500 avec la raison exacte, jamais un faux 503.
#
# A lancer depuis le dossier src/ du skill :
#   cd C:\Users\muse-build\work\amazon-bypass-maison\src
#   .\start.ps1

$ErrorActionPreference = "Continue"

$Python = "C:\Users\muse-build\work\tools\python-embed\python.exe"
$SkillDir = $PSScriptRoot

# V2 : le chemin des navigateurs n'est pas persistant sur le PC.
# Sans cette ligne, Playwright ne trouve pas Chromium.
if (-not $env:PLAYWRIGHT_BROWSERS_PATH) {
    $env:PLAYWRIGHT_BROWSERS_PATH = "C:\Users\muse-build\work\tools\ms-playwright"
}
$ApiKeyFile = Join-Path $SkillDir "api-key"
$ServerLog = Join-Path $SkillDir "server.log"
$ServerErrLog = Join-Path $SkillDir "server-err.log"

if (-not (Test-Path $Python)) {
    Write-Host "STOP : Python portable introuvable : $Python"
    exit 1
}

if (-not (Test-Path $ApiKeyFile)) {
    Write-Host "Generation de la cle API locale..."
    $ApiKey = (& $Python -c "import secrets; print(secrets.token_hex(32))").Trim()
    if ($LASTEXITCODE -ne 0 -or -not $ApiKey) {
        Write-Host "STOP : generation de la cle API echouee"
        exit 1
    }
    $ApiKey | Out-File -FilePath $ApiKeyFile -Encoding ascii -NoNewline
    Write-Host "Cle API generee, longueur $($ApiKey.Length), jamais affichee"
} else {
    $ApiKey = (Get-Content -Path $ApiKeyFile -Raw).Trim()
    Write-Host "Cle API lue depuis api-key, longueur $($ApiKey.Length), jamais affichee"
}

$env:AMAZON_API_KEY = $ApiKey
if (-not $env:AMAZON_DEFAULT_REGION) { $env:AMAZON_DEFAULT_REGION = "ca" }
$env:HOST = "127.0.0.1"
$env:PORT = "8792"
if (-not $env:AMAZON_COOKIE_DIR) { $env:AMAZON_COOKIE_DIR = Join-Path $SkillDir "cookies" }
$CookieFiles = Get-ChildItem -Path $env:AMAZON_COOKIE_DIR -Filter "cookies-*.txt" -ErrorAction SilentlyContinue
if (-not $CookieFiles) {
    Write-Host "ATTENTION : aucun jar de cookies dans $($env:AMAZON_COOKIE_DIR) - la recherche passera, mais le panier repondra 409. Exportez les cookies du navigateur (format Netscape) dans ce dossier : cookies-personal.txt pour le compte personnel, ou pointez AMAZON_COOKIE_DIR vers le dossier qui contient le jar avant de lancer ce script."
}

Write-Host "Demarrage du serveur Harbor Amazon sur 127.0.0.1:8792..."
$Server = Start-Process -FilePath $Python -ArgumentList @("-m", "harbor_amazon") `
    -WorkingDirectory $SkillDir -RedirectStandardOutput $ServerLog `
    -RedirectStandardError $ServerErrLog -PassThru -WindowStyle Hidden
if (-not $Server) {
    Write-Host "STOP : Start-Process n'a pas demarre le serveur"
    exit 1
}

$Up = $false
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Seconds 1
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8792/health" -UseBasicParsing -TimeoutSec 3
        if ($r.StatusCode -eq 200) { $Up = $true; break }
    } catch { }
    if ($Server.HasExited) {
        Write-Host "STOP : le serveur s'est arrete. Voir server.log et server-err.log :"
        if (Test-Path $ServerErrLog) { Get-Content -Path $ServerErrLog -Raw | Write-Host }
        exit 1
    }
}

if (-not $Up) {
    Write-Host "STOP : /health ne repond pas apres 20 s. Arret du serveur."
    if (-not $Server.HasExited) { Stop-Process -Id $Server.Id -Force }
    if (Test-Path $ServerErrLog) { Get-Content -Path $ServerErrLog -Raw | Write-Host }
    exit 1
}

Write-Host "Serveur en ligne : http://127.0.0.1:8792/health 200 (PID $($Server.Id))"
Write-Host "Le serveur reste en marche. Pour l'arreter : Stop-Process -Id $($Server.Id)"
