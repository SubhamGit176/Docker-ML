# Interactive chat client for your local llm-app (Flask + Ollama)
# Usage: .\chat.ps1

$Uri = "http://localhost:8080/chat"

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host " Local LLM Chat  (type 'exit' or 'quit' to stop)" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

while ($true) {
    $prompt = Read-Host "You"

    if ([string]::IsNullOrWhiteSpace($prompt)) {
        continue
    }

    if ($prompt -in @("exit", "quit")) {
        Write-Host "Goodbye." -ForegroundColor Yellow
        break
    }

    $payload = @{ prompt = $prompt } | ConvertTo-Json -Compress

    try {
        $response = Invoke-RestMethod -Uri $Uri -Method Post -Body $payload -ContentType "application/json"
        Write-Host "Bot: $($response.reply)" -ForegroundColor Green
        Write-Host ""
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
    }
}