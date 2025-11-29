# Offline RAG Chatbot Quickstart (Windows)

Clear-Host
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          Offline RAG Chatbot - Quickstart 🤖               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "  Activating virtual environment..." -ForegroundColor Yellow
$venvPath = ".\venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "  Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Virtual environment not found." -ForegroundColor Yellow
    Write-Host "  You can create it with:" -ForegroundColor Yellow
    Write-Host "    python -m venv venv" -ForegroundColor Gray
    Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "    pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " MODE: OFFLINE (NO API KEYS, DUMMY ANSWERS)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note:" -ForegroundColor Yellow
Write-Host "  • No external APIs are called." -ForegroundColor Gray
Write-Host "  • Answers are dummy offline responses for demonstration." -ForegroundColor Gray
Write-Host ""

# Simple interactive Q&A loop
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " ASK QUESTIONS (type 'exit' or 'quit' to stop)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

while ($true) {
    $question = Read-Host " Your question"

    if ($question -eq "exit" -or $question -eq "quit") {
        Write-Host ""
        Write-Host " Goodbye! 👋" -ForegroundColor Green
        break
    }

    if ([string]::IsNullOrWhiteSpace($question)) {
        Write-Host "  Please enter a non-empty question." -ForegroundColor Yellow
        continue
    }

    Write-Host ""
    Write-Host "  Processing (offline dummy mode)..." -ForegroundColor Yellow
    Write-Host ""

    # Call the Python demo script (which is already offline-safe)
    python demo.py "$question" 2>$null

    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
}