#!/bin/bash
# run.sh - تشغيل التطبيق على الكمبيوتر

echo "🚀 تشغيل نظام ادارة العملاء..."

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    exit 1
fi

# تثبيت المتطلبات
if [ ! -d "venv" ]; then
    echo "📦 انشاء بيئة افتراضية..."
    python3 -m venv venv
fi

echo "📦 تثبيت المتطلبات..."
source venv/bin/activate
pip install -r requirements.txt

# تشغيل التطبيق
echo "🚀 تشغيل التطبيق..."
python main.py
