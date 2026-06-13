[app]

# (str) Title of your application
title = نظام ادارة العملاء

# (str) Package name
package.name = customermanager

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yourcompany

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,db,md,txt

# (list) List of inclusions using pattern matching
source.include_patterns = src/assets/*,src/**/*.py

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, venv, .git, __pycache__, .buildozer

# (list) Application requirements
requirements = python3,kivy==2.2.1,sqlite3,openpyxl,plyer,pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #2563EB

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use.
android.ndk_api = 21

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature which is not compatible with Python
android.allow_backup = False

# (bool) Use AndroidX support
android.enable_androidx = True

# (str) Android app entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Gradle dependencies to add
android.gradle_dependencies = com.android.support:support-compat:28.0.0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
