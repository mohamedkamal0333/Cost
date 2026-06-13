#!/bin/bash
# buildozer.sh - سكريبت بناء APK بسيط

echo "=================================="
echo "  بناء APK - نظام ادارة العملاء"
echo "=================================="
echo ""

# التحقق من وجود buildozer
if ! command -v buildozer &> /dev/null; then
    echo "❌ buildozer غير مثبت!"
    echo "قم بتثبيته: pip install buildozer"
    exit 1
fi

# تنظيف البناء السابق
echo "🧹 تنظيف البناء السابق..."
buildozer android clean

# بناء APK debug
echo "🔨 بناء APK..."
buildozer android debug

# التحقق من النجاح
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ تم بناء APK بنجاح!"
    echo "📁 الملف موجود في: bin/"
    ls -lh bin/*.apk
else
    echo ""
    echo "❌ فشل البناء!"
    echo "تحقق من سجلات الاخطاء"
fi
