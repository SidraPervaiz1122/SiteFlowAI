# PowerShell script to reset demo database to clean initial state
Write-Host "Resetting SiteFlow AI Demo Database..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" -m backend.db.seed
Write-Host "SiteFlow AI database reset complete. Exact 24 BOQ items ready." -ForegroundColor Green
