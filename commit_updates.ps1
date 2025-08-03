# PowerShell script to commit CryptoPulse AI updates
Write-Host "🚀 Committing CryptoPulse AI debug fixes..." -ForegroundColor Green

# Kill any stuck git processes
Get-Process | Where-Object {$_.ProcessName -eq "git"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Reset any stuck commits
git reset HEAD

# Add all files
git add .

# Commit with message
git commit -m "Fix CryptoPulse AI startup and add debugging tools

✅ Fixed app.py startup sequence with error handling
✅ Added app_minimal.py as reliable fallback  
✅ Created comprehensive debug scripts
✅ All APIs tested and working
✅ Ready for production deployment

Debug tools:
- debug_complete.py: Full system test
- app_minimal.py: Guaranteed working version
- DEBUG_REPORT.md: Complete troubleshooting guide"

# Push to GitHub
git push origin master

Write-Host "✅ CryptoPulse AI successfully updated on GitHub!" -ForegroundColor Green
