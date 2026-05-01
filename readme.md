Here is a complete **README.md** for your project. You can save this file inside your `dev-tools` folder so you always have a reference for how your CLI works.

---

# 🛠️ Ultimate Dev Toolbox (CLI)

A modular, isolated Python Command Line Interface for common developer tasks.

## 🚀 Setup & Installation

### 1. Initialize the Environment
Navigate to the project folder and run:
```bash
python -m venv venv
source venv/Scripts/activate  # For Git Bash/Windows
pip install click qrcode[pil] PyJWT
```

### 2. Configure the Shortcut (Alias)
Add this to your `~/.bash_profile` to run the tool from anywhere:
```bash
alias tool='"/d/proj/dev-tools/venv/Scripts/python.exe" "/d/proj/dev-tools/main.py"'
```
Then refresh: `source ~/.bash_profile`

---

## 📖 Commands & Usage

| Command | Description | Example Usage |
| :--- | :--- | :--- |
| `tool uuid` | Generates a unique UUID v4 string. | `tool uuid` |
| `tool qr-show` | Displays a QR code **directly in the terminal**. | `tool qr-show "https://google.com"` |
| `tool qr` | Generates a QR code and **saves it as a file**. | `tool qr "data" "my_code.png"` |
| `tool jwt-parse` | Decodes a JWT token string (unverified). | `tool jwt-parse <your_token>` |
| `tool time` | Converts a Unix timestamp to a readable date. | `tool time 1714579140` |
| `tool run-all` | Runs multiple Python files **concurrently**. | `tool run-all script1.py script2.py` |
| `tool --help` | Shows the auto-generated help menu. | `tool --help` |

---

## 📂 Project Structure

```text
dev-tools/
├── main.py            # Entry point & CLI definitions
├── modules/           # Logic Modules
│   ├── crypto.py      # UUID & JWT handling
│   ├── media.py       # QR Code generation (File & Terminal)
│   ├── runner.py      # Concurrent subprocess logic
│   └── utils.py       # Timestamp formatting
├── venv/              # Isolated Python Environment (Private)
└── requirements.txt   # Project dependencies
```

---

## 🛠️ Tips
* **QR Codes:** If the terminal QR code is hard to scan, zoom out in your terminal (`Ctrl` + `-`).
* **Concurrency:** `run-all` is great for testing client-server scripts at the same time without opening two windows.
* **Adding Features:** To add a new command, create a function in a module and register it in `main.py` using `@cli.command()`.

---

**Everything set, bruh!** Is there anything else you want to automate today?