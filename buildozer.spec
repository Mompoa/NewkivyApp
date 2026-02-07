[app]

title = hello
package.name = king
package.domain = reng.app

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,gif

requirements = python3,pygame   # ← mas simple at stable

presplash.filename = %(source.dir)s/loading.png   # PNG mas safe kaysa GIF
icon.filename = %(source.dir)s/logo.png

version = 0.1

orientation = portrait
fullscreen = 1

# ————————————————
# Android settings
# ————————————————

android.api = 34          # or 35 — mas future-proof (subukan muna 34)
android.minapi = 21       # pwede iwan, o itaas sa 24 kung may problema
android.sdk = 34          # dapat match sa android.api
android.ndk = 25b         # pwede iwan o subukan 26 / alisin para auto
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.debug_artifact = apk
android.release_artifact = aab

android.accept_sdk_license = True
# ← tanggalin storage kung hindi talaga kailangan

android.bootstrap = sdl2
android.enable_androidx = True
android.internet = True


[buildozer]

log_level = 2
warn_on_root = 1
