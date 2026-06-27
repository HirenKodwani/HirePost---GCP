param(
    [string]$Port = "8080",
    [switch]$Reload = $true
)

$reloadFlag = ""
if ($Reload) {
    $reloadFlag = "--reload"
}

Set-Location -LiteralPath "$PSScriptRoot\..\backend"
uvicorn app.main:app --host 127.0.0.1 --port $Port $reloadFlag
