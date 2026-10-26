[app]

# (str) Title of your application
title = Yu-Gi-Oh! LP Tracker

# (str) Package name
package.name = yugiohlptracker

# (str) Package domain (needed for android packaging)
package.domain = org.cipher

# (str) Source files to include (let separate with commas)
source.include_exts = py,png,jpg,kv,atlas

# (str) Source directory where you live
source.dir = .

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations (portrait, landscape or all)
orientation = portrait

# (list) Permissions
#android.permissions = INTERNET

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.png

# (str) Supported orientations
osx.python_version = 3
osx.kivy_version = 1.11.0

# ---- Android specific ----
[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
