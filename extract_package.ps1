# Extract GPT-SoVITS Package Script

$archivePath = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228.7z"
$extractPath = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Extract GPT-SoVITS Package" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if file exists
if (-not (Test-Path $archivePath)) {
    Write-Host "Error: Package file not found: $archivePath" -ForegroundColor Red
    exit 1
}

Write-Host "Found package file: $archivePath" -ForegroundColor Green

# Check if already extracted
if (Test-Path $extractPath) {
    Write-Host "Target directory already exists: $extractPath" -ForegroundColor Yellow
    $response = Read-Host "Delete existing directory and re-extract? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        Remove-Item -Path $extractPath -Recurse -Force
        Write-Host "Deleted existing directory" -ForegroundColor Green
    } else {
        Write-Host "Skipping extraction, using existing directory" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "Attempting to extract..." -ForegroundColor Yellow

# Method 1: Try 7-Zip
$sevenZipPaths = @(
    "C:\Program Files\7-Zip\7z.exe",
    "C:\Program Files (x86)\7-Zip\7z.exe",
    "$env:ProgramFiles\7-Zip\7z.exe",
    "$env:ProgramFiles(x86)\7-Zip\7z.exe"
)

$sevenZipFound = $false
foreach ($path in $sevenZipPaths) {
    if (Test-Path $path) {
        Write-Host "Found 7-Zip: $path" -ForegroundColor Green
        Write-Host "Extracting, please wait..." -ForegroundColor Yellow
        
        $process = Start-Process -FilePath $path -ArgumentList "x", "`"$archivePath`"", "-o`"$extractPath`"", "-y" -Wait -NoNewWindow -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Extraction successful!" -ForegroundColor Green
            $sevenZipFound = $true
            break
        } else {
            Write-Host "7-Zip extraction failed, exit code: $($process.ExitCode)" -ForegroundColor Red
        }
    }
}

if ($sevenZipFound) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Extraction Complete!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Extracted to: $extractPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Navigate to extracted directory:" -ForegroundColor White
    Write-Host "   cd `"$extractPath`"" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Start WebUI:" -ForegroundColor White
    Write-Host "   .\go-webui.bat" -ForegroundColor Gray
    Write-Host "   Or double-click go-webui.bat" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Browser will open automatically" -ForegroundColor White
    Write-Host ""
    exit 0
}

# Method 2: Manual extraction instructions
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  7-Zip not found, please extract manually" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Please use one of the following methods:" -ForegroundColor White
Write-Host ""
Write-Host "Method 1: Install 7-Zip and run this script again" -ForegroundColor Cyan
Write-Host "  Download: https://www.7-zip.org/download.html" -ForegroundColor Gray
Write-Host ""
Write-Host "Method 2: Use WinRAR (if installed)" -ForegroundColor Cyan
Write-Host "  Right-click file -> Extract to GPT-SoVITS-v3lora-20250228\" -ForegroundColor Gray
Write-Host ""
Write-Host "Method 3: Use Windows 11 built-in extraction" -ForegroundColor Cyan
Write-Host "  Right-click file -> Extract All" -ForegroundColor Gray
Write-Host ""
Write-Host "Method 4: Use other extraction tools" -ForegroundColor Cyan
Write-Host "  - Bandizip: https://www.bandisoft.com/bandizip/" -ForegroundColor Gray
Write-Host "  - PeaZip: https://peazip.github.io/" -ForegroundColor Gray
Write-Host ""
Write-Host "Extract to: $extractPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "After extraction, run:" -ForegroundColor White
Write-Host "  cd `"$extractPath`"" -ForegroundColor Gray
Write-Host "  .\go-webui.bat" -ForegroundColor Gray
Write-Host ""

