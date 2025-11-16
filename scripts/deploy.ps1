# BrandGuard Deployment Script for Windows
# This script sets up and deploys BrandGuard using Docker Compose

Write-Host "🚀 Starting BrandGuard Deployment..." -ForegroundColor Green

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
try {
    docker compose version | Out-Null
} catch {
    Write-Host "❌ Docker Compose is not available. Please ensure Docker Desktop is running." -ForegroundColor Red
    exit 1
}

# Create environment file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating environment file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your production values before continuing." -ForegroundColor Yellow
    Write-Host "Press any key to continue once you've configured .env..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Build and start services
Write-Host "🏗️  Building Docker images..." -ForegroundColor Blue
docker compose build --no-cache

Write-Host "🚀 Starting services..." -ForegroundColor Blue
docker compose up -d

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Blue
docker compose ps

# Show logs
Write-Host "📋 Recent logs:" -ForegroundColor Blue
docker compose logs --tail=20

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your BrandGuard application is now running at:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 To monitor logs: docker compose logs -f" -ForegroundColor Yellow
Write-Host "🛑 To stop: docker compose down" -ForegroundColor Yellow
Write-Host "🔄 To restart: docker compose restart" -ForegroundColor Yellow