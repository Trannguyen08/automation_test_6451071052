$ErrorActionPreference = "Stop"

$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$reportDirectory = [IO.Path]::GetFullPath((Join-Path $workspace "report"))
$resultsDirectory = [IO.Path]::GetFullPath((Join-Path $reportDirectory "allure-results"))
$expectedResultsDirectory = [IO.Path]::GetFullPath(
    (Join-Path $workspace "report\allure-results")
)

if (-not $resultsDirectory.Equals($expectedResultsDirectory, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Đường dẫn allure-results không hợp lệ: $resultsDirectory"
}

if (-not $resultsDirectory.StartsWith(
    $reportDirectory + [IO.Path]::DirectorySeparatorChar,
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw "Từ chối xóa thư mục ngoài report: $resultsDirectory"
}

if (Test-Path -LiteralPath $resultsDirectory -PathType Container) {
    Remove-Item -LiteralPath $resultsDirectory -Recurse -Force
    Write-Output "Da xoa du lieu tam: $resultsDirectory"
}
