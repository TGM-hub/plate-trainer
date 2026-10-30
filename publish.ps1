# Publie le trainer sur GitHub : aperçu de ce qui part, confirmation, commit, push.
# Lancement : double-clic sur publish.cmd (ou powershell -ExecutionPolicy Bypass -File .\publish.ps1)
# Trainer statique (index.html autonome) : pas de build. Repo et Pages existent déjà.

$ErrorActionPreference = "Continue"   # PowerShell 5.1 : "Stop" rend fatal le stderr de git
Set-Location $PSScriptRoot
git config core.quotepath false
$branch = git branch --show-current
$remote = git remote get-url origin
$name = ($remote -replace '\.git$', '') -replace '^.*/', ''
$url = "https://tgm-hub.github.io/$name/"

# 1. Se mettre à jour avec GitHub (évite de repartir d'une copie en retard)
git fetch -q origin
$behind = git rev-list --count "HEAD..origin/$branch"
if ($behind -ne "0") {
    Write-Host "La copie locale a $behind commit(s) de retard sur GitHub." -ForegroundColor Yellow
    git pull --rebase --autostash -q origin $branch
    if ($LASTEXITCODE -ne 0) { throw "git pull a échoué : règle le conflit avant de publier." }
}

# 2. Aperçu
git add -A
$staged = git diff --cached --name-status
$ahead = git rev-list --count "origin/$branch..HEAD"
if (-not $staged -and $ahead -eq "0") { Write-Host "`nRien de nouveau à publier."; exit 0 }
if ($staged) {
    Write-Host "`nFichiers qui vont partir :" -ForegroundColor Cyan
    $staged | ForEach-Object { Write-Host "  $_" }
    Write-Host "`nDétail :" -ForegroundColor Cyan
    git diff --cached --stat
} else {
    Write-Host "`nCommits locaux pas encore poussés :" -ForegroundColor Cyan
    git log --oneline "origin/$branch..HEAD"
}
if ((Read-Host "`nPublier sur $name ($branch) ? (o/N)") -notmatch '^[oOyY]') { git reset -q; Write-Host "Annulé, rien n'est parti."; exit 1 }

# 3. Commit et push
if ($staged) {
    $msg = Read-Host ("Message de commit (Entrée = « Mise à jour {0:yyyy-MM-dd} »)" -f (Get-Date))
    if (-not $msg) { $msg = "Mise à jour {0:yyyy-MM-dd}" -f (Get-Date) }
    git commit -q -m $msg -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    if ($LASTEXITCODE -ne 0) { throw "git commit a échoué" }
}
git push origin $branch
if ($LASTEXITCODE -ne 0) { throw "git push a échoué (voir le message ci-dessus)" }
Write-Host "`nPublié. En ligne d'ici une minute : $url" -ForegroundColor Green
