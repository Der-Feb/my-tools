# 🛠️ Ultimate Dev Toolbox

A powerful, modular Python CLI designed for developers. Handle QR codes, JWTs, timestamps, and file conversions with ease.

---

## 🚀 Installation & Setup

### 1. Initialize Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### 2. Configure Global Access
Add this alias to your `~/.bashrc` or `~/.bash_profile` to use the tool from any directory:
```bash
alias tool='python d:/proj/my-tools/main.py'
```

---

## 📖 Command Reference

### 1. 📱 QR Code Tool (`qr`)
Generate, show, or scan QR codes instantly.
- **Show in Terminal**: `tool qr "https://github.com" -s`
- **Save to File**: `tool qr "Secret Data" -f code.png`
- **Parse/Scan**: `tool qr -p screenshot.png`

### 2. 🔐 JWT Tool (`jwt`)
The Swiss Army knife for JSON Web Tokens.
- **Decode**: `tool jwt <token>` (Auto-converts `exp`/`iat` to readable dates)
- **Verify**: `tool jwt <token> -v "your-secret"`
- **Create**: `tool jwt -C -F payload.json -v "your-secret"`
- **Algorithm**: Default is HS256, auto-detects for decoding.

### 3. ⏰ Time Tool (`time`)
Precision time conversion and timestamp generation.
- **Current Time**: `tool time -n`
- **Timestamp -> Date**: `tool time -r 1781097394`
- **Date -> Timestamp**: `tool time -t "2026-12-25"`
- **Millisecond Precision**: Add `--ms` to any command for 13-digit precision.

### 4. 📄 Converter Tool (`convert`)
Batch convert documents to PDF without opening heavy apps.
- **Word to PDF**: `tool convert document.docx`
- **PowerPoint to PDF**: `tool convert slides.pptx`
- **Batch Directory**: `tool convert ./my_docs`
- **Advanced Flags**:
  - `-d`: Delete original file after successful conversion.
  - `-e "exclude|these"`: Skip specific files during batch conversion.

### 5. 🔗 URL Parser (`url`)
Break down complex URLs into readable components.
- **Usage**: `tool url "https://user:pass@example.com:8080/p/a/t/h?query=1#frag"`

### 6. 🆔 UUID Generator (`uuid`)
- **Usage**: `tool uuid -n 5`

---

## 🛠️ Advanced Features
- **Global `-h`**: Use `-h` on any command for specific help and examples.
- **Grep Friendly**: All outputs use consistent labels (e.g., `QR Data:`, `Unix Timestamp:`) for easy piping.
- **Mutually Exclusive Flags**: Prevents conflicting commands (e.g., can't parse and generate at the same time).

---

## 📂 Project Structure
- [main.py](file:///d:/proj/my-tools/main.py): Entry point & CLI definitions.
- [modules/crypto.py](file:///d:/proj/my-tools/modules/crypto.py): JWT & UUID logic.
- [modules/media.py](file:///d:/proj/my-tools/modules/media.py): QR code generation/parsing.
- [modules/converter.py](file:///d:/proj/my-tools/modules/converter.py): Word/PPT to PDF logic.
- [modules/utils.py](file:///d:/proj/my-tools/modules/utils.py): URL parsing & Time formatting.

---
**Crafted with 🚀 for developers.**
