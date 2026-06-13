# نظام ادارة العملاء - Customer Manager

تطبيق اندرويد كامل لادارة العملاء والمدفوعات باستخدام Kivy و Python.

## المميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| ✅ واجهة عربية احترافية | تصميم عصري للموبايل |
| ✅ قاعدة بيانات SQLite | تخزين محلي بدون انترنت |
| ✅ CRUD كامل | اضافة - تعديل - حذف العملاء |
| ✅ بحث متقدم | بالاسم او رقم الهاتف |
| ✅ تسجيل المدفوعات | تتبع المدفوع والمتبقي |
| ✅ تنبيهات التجديد | اشعارات بمواعيد التجديد |
| ✅ احصائيات تلقائية | حساب اجمالي المبالغ |
| ✅ تصدير البيانات | Excel و CSV |
| ✅ APK جاهز | قابل للبناء مباشرة |

## هيكل المشروع

```
CustomerManager/
├── main.py                      # نقطة الدخول الرئيسية
├── customer_manager.kv          # ملف التصميم
├── buildozer.spec               # اعدادات بناء APK
├── buildozer.sh / .bat          # سكريبتات البناء
├── run.sh                       # سكريبت التشغيل
├── requirements.txt             # المتطلبات
├── README.md                    # هذا الملف
├── .gitignore                   # استثناءات Git
│
├── src/
│   ├── __init__.py
│   │
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── home_screen.py       # الشاشة الرئيسية (لوحة المعلومات)
│   │   ├── customers_screen.py  # قائمة العملاء
│   │   ├── add_customer_screen.py    # اضافة عميل
│   │   ├── edit_customer_screen.py   # تعديل عميل
│   │   ├── payments_screen.py   # تسجيل المدفوعات
│   │   ├── reports_screen.py    # التقارير والتصدير
│   │   ├── search_screen.py     # البحث المتقدم
│   │   └── settings_screen.py   # الاعدادات
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py          # ادارة قاعدة البيانات
│   │   ├── notifications.py     # التنبيهات والاشعارات
│   │   └── export_manager.py    # تصدير Excel/CSV
│   │
│   └── assets/
│       └── fonts/
│           └── Cairo-Regular.ttf  # خط عربي (اختياري)
```

## طريقة التشغيل على الكمبيوتر

### المتطلبات
- Python 3.8+
- pip

### التثبيت والتشغيل

```bash
# 1. فك ضغط المشروع
cd CustomerManager

# 2. انشاء بيئة افتراضية (مستحسن)
python3 -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. تشغيل التطبيق
python main.py
```

او استخدم السكريبت الجاهز:
```bash
# Linux/Mac:
chmod +x run.sh
./run.sh

# Windows:
run.bat
```

## بناء ملف APK للاندرويد

### الطريقة 1: باستخدام Buildozer على Linux

```bash
# 1. تثبيت المتطلبات
sudo apt update
sudo apt install -y python3-pip build-essential git ffmpeg \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
    libfreetype6-dev libgl1-mesa-dev libgles2-mesa-dev

# 2. تثبيت Buildozer
pip3 install --user buildozer cython

# 3. الانتقال الى مجلد المشروع
cd CustomerManager

# 4. بناء APK debug
buildozer android debug

# 5. سيتم انشاء الملف في:
# bin/customermanager-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### الطريقة 2: باستخدام Docker (اسهل)

```bash
# 1. الانتقال الى مجلد المشروع
cd CustomerManager

# 2. تشغيل Buildozer عبر Docker
docker run --interactive --tty --rm \
  --volume "$(pwd)":/home/user/hostcwd \
  --workdir /home/user/hostcwd \
  kivy/buildozer android debug

# 3. سيتم انشاء APK في مجلد bin/
```

### الطريقة 3: باستخدام Google Colab (مجاني - اسهل طريقة)

1. افتح [Google Colab](https://colab.research.google.com/)
2. انشاء خلية جديدة والصق الكود التالي:

```python
# تثبيت المتطلبات
!pip install buildozer cython

# رفع ملف ZIP
from google.colab import files
uploaded = files.upload()

# فك الضغط
!unzip CustomerManager.zip

# بناء APK
!cd CustomerManager && buildozer android debug

# تحميل APK
import glob
apk_files = glob.glob('CustomerManager/bin/*.apk')
if apk_files:
    files.download(apk_files[0])
```

3. اضغط "تشغيل" وانتظر حتى ينتهي البناء
4. سيظهر زر تحميل APK

### الطريقة 4: باستخدام GitHub Actions (CI/CD)

انشاء ملف `.github/workflows/build.yml`:

```yaml
name: Build APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y python3-pip build-essential git
          pip install buildozer cython

      - name: Build APK
        run: buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: app-debug
          path: bin/*.apk
```

## صلاحيات التطبيق

| الصلاحية | الغرض |
|----------|-------|
| INTERNET | تحديثات مستقبلية |
| WRITE_EXTERNAL_STORAGE | تصدير البيانات |
| READ_EXTERNAL_STORAGE | استيراد البيانات |
| ACCESS_NETWORK_STATE | التحقق من الاتصال |

## جدول قاعدة البيانات

### جدول العملاء (customers)
| العمود | النوع | الوصف |
|--------|-------|-------|
| id | INTEGER | معرف فريد |
| name | TEXT | اسم العميل |
| phone | TEXT | رقم الهاتف |
| email | TEXT | البريد الالكتروني |
| address | TEXT | العنوان |
| service_type | TEXT | نوع الخدمة |
| amount | REAL | المبلغ الكلي |
| paid_amount | REAL | المبلغ المدفوع |
| remaining_amount | REAL | المبلغ المتبقي |
| start_date | TEXT | تاريخ البدء |
| end_date | TEXT | تاريخ الانتهاء |
| renewal_date | TEXT | تاريخ التجديد |
| notes | TEXT | ملاحظات |
| status | TEXT | الحالة |

### جدول المدفوعات (payments)
| العمود | النوع | الوصف |
|--------|-------|-------|
| id | INTEGER | معرف فريد |
| customer_id | INTEGER | رقم العميل |
| amount | REAL | المبلغ |
| payment_date | TEXT | تاريخ الدفع |
| payment_method | TEXT | طريقة الدفع |
| notes | TEXT | ملاحظات |

## الاعدادات

يمكن تعديلها من شاشة الاعدادات:

| الاعداد | الافتراضي | الوصف |
|---------|-----------|-------|
| company_name | شركتي | اسم الشركة |
| currency | ريال | العملة |
| renewal_days | 7 | ايام التنبيه |
| backup_enabled | 1 | تفعيل النسخ الاحتياطي |

## حل المشاكل الشائعة

### مشكلة: التطبيق لا يعمل على الكمبيوتر
```bash
# التأكد من تثبيت Kivy
pip install kivy[base]

# اذا استمرت المشكلة
pip install --upgrade kivy
```

### مشكلة: فشل بناء APK
```bash
# تنظيف واعادة البناء
buildozer android clean
buildozer android debug

# او استخدام verbose
buildozer -v android debug
```

### مشكلة: الخط العربي لا يظهر
- ضع ملف `Cairo-Regular.ttf` في `src/assets/fonts/`
- او عدل `main.py` لاستخدام خط النظام

### مشكلة: قاعدة البيانات
- الملف يُنشأ تلقائيا في اول تشغيل
- على Android: في مجلد التطبيق
- على الكمبيوتر: في `~/.customer_manager/`

## الترخيص

MIT License - حر الاستخدام

## الدعم

للاسئلة والاقتراحات، يرجى فتح Issue.
