# 🐍 Python Script Collection

A collection of utility Python scripts. Currently includes:

- `organise.py`: Automatically organizes files in a directory based on file type.
- `imgCompressor.py`: Smartly compresses images in your computer also specific handling for folderName = `Resume` where it creates separate img versions for`<0.5mb, <1mb, <2mb, original`
Also for creatives out there it checks for folderName = `footage` and makes sure not to touch since we need the highest quality when we need to edit for future creatives.
- Yes I didn't forget my Editor friend's out there.🤩
- More scripts will be added soon.
- This repository supports cross-platform automation on **macOS**, **Windows**, and **Linux**.

---

## 📂 Scripts Overview

| Script Name      | Description                           |
| ---------------- | ------------------------------------- |
| organise.py      | Organizes files by type into folders. |
| imgCompressor.py | Smartly compresses img's in your mac. |

---

## Note

- This current approach for `imgCompressor` utilizes a `tracking_db.json` which essentially creates a local database for checking whether a file has been already optimzed because we don't want to iteratively degrade our image's quality every iteration.
- This approach makes use of MD5 hashing ensuring that until unless the image was edited explicity it will not be considered for a re-optimize. And will not fail for a image-rename or location-move from one place to Another.
- So in the event you want to get rid of the original files make sure not to delete `image_optimizer.log` and `tracking_db.json` file otherwise you guessed it our script will not find the database hence everything will be queued for a re-optimization.

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
```

</details>

2. **Place the plist file**:

```bash
cp com.username.organise.plist ~/Library/LaunchAgents/
```

3. **Load the script**:

```bash
launchctl load ~/Library/LaunchAgents/com.username.organise.plist
```

4. **Check logs**:

```bash
tail -f /tmp/organise.log
```

> ✅ **Note**: Ensure the script has executable permissions:
> ```bash
> chmod +x organise.py
> ```

---

### 🩟 Windows (via Task Scheduler)

1. Open **Task Scheduler**.
2. Create a **Basic Task**:
   - Action: `Start a program`
   - Program/script: Path to `python.exe`
   - Add arguments: `"C:\path\to\organise.py"`
3. Set trigger time (e.g., daily/hourly).
4. Make sure Python is added to your system `PATH`.

---

### 🐧 Linux (via `cron`)

1. Open crontab:

```bash
crontab -e
```

2. Add the following line to run the script every hour:

```bash
0 * * * * /usr/bin/python3 /home/user/path/to/organise.py >> /home/user/organise.log 2>&1
```

3. Save and exit. Check logs at:

```bash
tail -f /home/user/organise.log
```

---

## 🧪 Environment Setup

You can run the scripts either **globally** or within a **virtual environment**.

### ✅ Global

Make sure Python is installed globally and available in your system’s PATH.

```bash
python3 organise.py
```

### 📦 Virtual Environment

Recommended for better dependency management.

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python organise.py
```

---

## 🛠️ Other Libraries & Tools

In addition to native schedulers, you can also consider these:

- **APScheduler** – Python-based advanced job scheduling.
- **Celery + Redis** – For distributed task queues.
- **Watchdog** – Monitor directories for real-time changes.
- **Systemd timers** (Linux) – Alternative to cron.

---

## ⚠️ Common Points of Failure

| Issue                              | Solution                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| Permission denied                  | Ensure scripts have execution rights (`chmod +x`).                                   |
| Not running at scheduled time      | Double-check scheduler setup and time zones.                                         |
| Python not found                   | Use absolute path to Python binary.                                                  |
| Script not triggering              | Check logs (`/tmp/*.log` or custom paths).                                           |
| Environment errors                 | Activate virtual environment or fix `PATH`.                                          |
| Launchctl: Operation not permitted | Add full disk access in **System Settings → Privacy & Security → Full Disk Access**. |

---

## 📄 Logging

Make sure each script logs both **stdout** and **stderr**:

Inside your Python script:

```python
import logging

logging.basicConfig(
    filename='/tmp/organise.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

try:
    # your script logic here
    logging.info("Script started.")
except Exception as e:
    logging.error("Error occurred", exc_info=True)
```

---

## 🧠 Contribution & Usage

This repo is evolving with more scripts to be added soon.

- ✅ Feel free to fork and use.
- 🔁 Submit PRs if you'd like to contribute.
- ⭐ Star the repo if it helped you.

---

Made with ❤️ by Chirag Dahiya

