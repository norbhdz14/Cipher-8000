[app]
title = Yu-Gi-Oh! LP Tracker
package.name = yugiohlptracker
package.domain = org.cipher
version = 1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy==2.3.0
orientation = portrait
icon.filename = %(source.dir)s/logo.png

# Android
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
#android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
