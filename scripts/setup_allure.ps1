$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$allureVersion = "2.46.1"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$toolsDirectory = Join-Path $workspace ".tools"
$allureDirectory = Join-Path $toolsDirectory "allure-$allureVersion"
$allureCommand = Join-Path $allureDirectory "bin\allure.bat"

if (-not (Test-Path -LiteralPath $allureCommand)) {
    New-Item -ItemType Directory -Force -Path $toolsDirectory | Out-Null
    $archive = Join-Path $toolsDirectory "allure-$allureVersion.zip"
    $downloadUrl = "https://github.com/allure-framework/allure2/releases/download/$allureVersion/allure-$allureVersion.zip"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $archive -UseBasicParsing
    Expand-Archive -LiteralPath $archive -DestinationPath $toolsDirectory -Force
    Remove-Item -LiteralPath $archive -Force
}

if (-not (Test-Path -LiteralPath $allureCommand)) {
    throw "Không tìm thấy Allure CLI sau khi cài đặt: $allureCommand"
}

Write-Output $allureCommand
