@echo off
chcp 65001 >nul
echo ==================================
echo   بناء APK - نظام ادارة العملاء
echo ==================================
echo.

REM التحقق من وجود buildozer
buildozer --version >nul 2>&1
if errorlevel 1 (
    echo ❌ buildozer غير مثبت!
    echo قم بتثبيته: pip install buildozer
    pause
    exit /b 1
)

echo 🧹 تنظيف البناء السابق...
buildozer android clean

echo 🔨 بناء APK...
buildozer android debug

if errorlevel 1 (
    echo.
    echo ❌ فشل البناء!
    pause
) else (
    echo.
    echo ✅ تم بناء APK بنجاح!
    echo 📁 الملف موجود في: bin\
    dir /b bin\*.apk
    pause
)
