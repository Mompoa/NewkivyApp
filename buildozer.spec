[app]

# (str) Title of your application
title = hello

# (str) Package name
package.name = king

# (str) Package domain (needed for android/ios packaging)
package.domain = reng.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,gif

# (list) Application requirements
requirements = python3,kivy,plyer,pygame 

# (str) Presplash of the application (optional)
presplash.filename = %(source.dir)s/loading.gif

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.png

# (str) Application version
version = 0.1

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# ------------------------------
#  UPDATED ANDROID SETTINGS
# ------------------------------

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK / AAB will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

# (str) The format used to package the app for release mode
android.release_artifact = aab

# (bool) Automatically accept Android SDK license agreements
android.accept_sdk_license = True

# (list) Android permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (bool) Use AndroidX support libraries
android.enable_androidx = True

# (bool) Allow internet access (default: True)
android.internet = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
