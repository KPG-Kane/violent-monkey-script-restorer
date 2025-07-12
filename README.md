# ViolentMonkey Script Restorer

Recover lost userscripts from Chrome/ViolentMonkey's internal LevelDB backups.

This tool extracts and restores your scripts from Chrome profile backups that contain ViolentMonkey's internal data (the `*.log` file).

---

## 🔧 How It Works

ViolentMonkey stores userscripts in Chrome’s internal **LevelDB** files under your user profile.

This tool:
- Scans `*.log` files for `==UserScript==` blocks
- Decodes escape sequences (`\n`, `\t`, etc.)
- Outputs individual `.js` files per script
- Handles multiple Chrome profiles and avoids filename clashes

---

## 📁 Where to Find Your Profile Backups

Chrome profiles are stored in:

```
C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\
```

Common subfolders include:
- `Default`
- `Profile 1`
- `Profile 2`
- `Profile <N>`

ViolentMonkey data is stored in each profile's:

```
<ProfileFolder>\Local Extension Settings\jinjaccalgkegednnccohejagnlnfdag\
```

> `jinjaccalgkegednnccohejagnlnfdag` is ViolentMonkey's extension ID.

Look for files like `000003.log`, `LOG`, or `MANIFEST-000001` in that folder.

---

## 📂 How to Prepare for Recovery

1. Create a `Backups/` folder in the same directory as the script
2. Inside `Backups/`, copy your Chrome 'jinjaccalgkegednnccohejagnlnfdag' folders and rename them (typically to match their parent folders: `Default`, `Profile 1`, etc.)
3. Make sure each profile folder contains a `.log` file from the `jinjaccalgkegednnccohejagnlnfdag` directory

Example layout:
```
Backups/
├── Default/
│   └── 000003.log
├── Profile 1/
│   └── 000002.log
```

---

## ▶️ How to Run

```bash
python restore_files.py
```

Scripts will be restored to:

```
recovered_scripts/
├── Default/
│   └── YourScript.user.js
├── Profile 1/
│   └── AnotherScript.user.js
```

---

## ✅ Requirements

- Python 3.6+
- No third-party libraries required

---

## 🛟 What It Recovers

- All userscripts with a `==UserScript==` block
- Script names and versions from metadata
- Code formatting and line breaks

---

## 📝 License

MIT
