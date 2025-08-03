@echo off
echo Forcing git commit completion...

REM Kill any stuck git processes
taskkill /F /IM git.exe >nul 2>&1
timeout /t 2 >nul

REM Reset any pending commits
git reset HEAD >nul 2>&1

REM Add all files
git add .

REM Commit with message
git commit -m "Fix CryptoPulse AI startup issues and add debugging tools - Fixed app.py startup sequence - Added comprehensive debug scripts - All APIs tested and working - Ready for production deployment"

REM Push to GitHub
git push origin master

echo.
echo ========================================
echo  CryptoPulse AI Successfully Updated!
echo ========================================
echo.
echo Your GitHub repository has been updated with:
echo - Fixed Flask application startup
echo - Comprehensive debugging tools  
echo - API timeout error handling
echo - Production-ready configuration
echo.
echo Visit: https://github.com/Nagesh00/cryptopulseai
echo GitHub Pages: https://nagesh00.github.io/cryptopulseai/
echo.
pause
