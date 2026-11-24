# One-click data refresh: new products -> translate/classify/validate -> Instagram events -> check.
# Same pipeline as the "한 번에 실행" button on the admin page. Reads ADMIN_TOKEN from .env and
# never prints it. Usage:  powershell -ExecutionPolicy Bypass -File scripts\collect_all.ps1 [-Steps events,verify]
param(
    [string[]]$Steps = @(),
    [string]$BaseUrl = 'http://127.0.0.1:8000'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root '.env'
if (-not (Test-Path $envFile)) { Write-Host '.env 파일이 없습니다.' -ForegroundColor Red; exit 1 }
$token = (Get-Content $envFile | Where-Object { $_ -match '^\s*ADMIN_TOKEN\s*=' } | Select-Object -First 1) -replace '^\s*ADMIN_TOKEN\s*=\s*', '' -replace '^["'']|["'']$', ''
if (-not $token) { Write-Host '.env에 ADMIN_TOKEN이 없습니다.' -ForegroundColor Red; exit 1 }
$headers = @{ 'X-Admin-Token' = $token }
$labels = @{ completed = '완료'; partial = '일부 완료'; skipped = '건너뜀'; failed = '실패'; running = '진행 중'; pending = '대기'; not_requested = '선택 안 함' }
function Get-Label($state) { if ($labels.ContainsKey($state)) { $labels[$state] } else { $state } }
# Windows PowerShell 5.1 decodes JSON without a charset as Latin-1; read the bytes as UTF-8 instead.
function Invoke-Api($Path, $Method = 'Get', $Body = $null) {
    $params = @{ Uri = "$BaseUrl$Path"; Method = $Method; Headers = $headers; UseBasicParsing = $true }
    if ($Body) { $params.ContentType = 'application/json; charset=utf-8'; $params.Body = [Text.Encoding]::UTF8.GetBytes($Body) }
    $response = Invoke-WebRequest @params
    [Text.Encoding]::UTF8.GetString($response.RawContentStream.ToArray()) | ConvertFrom-Json
}

$body = if ($Steps.Count) { @{ steps = $Steps } | ConvertTo-Json -Compress } else { '{}' }
try {
    $run = Invoke-Api '/api/admin/pipeline/run' 'Post' $body
} catch {
    Write-Host "백엔드에 연결할 수 없습니다 ($BaseUrl). Docker가 켜져 있는지, scripts\update.ps1로 최신 이미지를 반영했는지 확인하세요." -ForegroundColor Red
    exit 1
}
if ($run.reason -eq 'already_running') { Write-Host '이미 실행 중인 작업이 있습니다. 진행 상황을 이어서 표시합니다.' -ForegroundColor Yellow }

$last = ''
do {
    Start-Sleep -Seconds 3
    $run = Invoke-Api '/api/admin/pipeline'
    $line = ($run.steps | ForEach-Object { "$($_.label): $(Get-Label $_.state)" }) -join ' | '
    if ($line -ne $last) { Write-Host ("[{0:HH:mm:ss}] {1}" -f (Get-Date), $line); $last = $line }
} while ($run.state -eq 'running')

Write-Host ''
foreach ($s in $run.steps) {
    $facts = ($s.PSObject.Properties | Where-Object { $_.Value -is [int] -or $_.Value -is [long] } | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ', '
    $color = switch ($s.state) { 'completed' { 'Green' } 'failed' { 'Red' } default { 'Yellow' } }
    Write-Host ("{0,-14} {1,-6} {2} {3}" -f $s.label, (Get-Label $s.state), $facts, $s.reason) -ForegroundColor $color
}
Write-Host "`n전체 결과: $(Get-Label $run.state)"
if ($run.state -in 'completed', 'partial') { exit 0 } else { exit 1 }
