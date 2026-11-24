$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
function Run-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw 'Docker command failed. Read the output above; do not delete volumes.' }
}
if (!(Test-Path '.env')) { throw 'Copy your existing .env into this folder before updating.' }
Run-Docker compose -p figure-archive-ai up -d postgres chroma
Run-Docker compose -p figure-archive-ai stop backend frontend
Run-Docker compose -p figure-archive-ai build backend frontend
Run-Docker compose -p figure-archive-ai run --rm --no-deps backend alembic upgrade head
Run-Docker compose -p figure-archive-ai up -d --no-deps backend frontend
Run-Docker compose -p figure-archive-ai ps
Write-Host 'Update finished. Open http://localhost:8080 . Existing DB volume is preserved.'
