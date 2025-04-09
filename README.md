# 🐍 Python Script Collection

A collection of utility Python scripts. Currently includes:

- `organise.py`: Automatically organizes files in a directory based on file type.

More scripts will be added soon. This repository supports cross-platform automation on **macOS**, **Windows**, and **Linux**.

---

## 📂 Scripts Overview

| Script Name   | Description                            |
|--------------|----------------------------------------|
| organise.py  | Organizes files by type into folders.  |

---

## 🚀 Running the Scripts Automatically

### 🖥 macOS (via `launchctl`)

1. **Create a `.plist` file** (e.g., `com.username.organise.plist`):

<details>
<summary>Click to view sample</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.username.organise</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/yourname/path/to/organise.py</string>
    </array>

    <key>StartInterval</key>
    <integer>3600</integer> <!-- Run every hour -->

    <key>StandardOutPath</key>
    <string>/tmp/organise.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/organise.error.log</string>
</dict>
</plist>
