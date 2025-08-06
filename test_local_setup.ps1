# Test Local Setup
Write-Host "🧪 Testing Local Setup..." -ForegroundColor Green

$services = @(
    @{Name="Frontend"; URL="http://localhost:3000"; Expected="React App"},
    @{Name="Backend"; URL="http://localhost:5000/health"; Expected="healthy"},
    @{Name="Whisper API"; URL="http://localhost:5001/health"; Expected="healthy"}
)

foreach ($service in $services) {
    Write-Host "`n🔍 Testing $($service.Name)..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri $service.URL -Method GET -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($service.Name) is running" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $($service.Name) responded with status $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($service.Name) is not running or not accessible" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "If all services show ✅, your local setup is working!" -ForegroundColor Green
Write-Host "If any show ❌, start the missing service using the commands from start_local.ps1" -ForegroundColor Yellow 