Write-Host "🔧 Fixing railway_prep.py location..."

$CurrentDir = Get-Location
$ParentDir = Split-Path $CurrentDir -Parent
$ScriptPath = Join-Path $CurrentDir "railway_prep.py"
$TargetPath = Join-Path $ParentDir "railway_prep.py"

if (-Not (Test-Path $ScriptPath)) {
    Write-Host "❌ railway_prep.py not found in this folder."
    exit
}

Move-Item $ScriptPath $TargetPath -Force

Write-Host "✅ railway_prep.py moved to repo root."
Write-Host "📁 New location: $TargetPath"
Write-Host ""
Write-Host "You can now run:"
Write-Host "python railway_prep.py"
