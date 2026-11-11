# 🔐 Secure Image Steganography

> **Encrypt a secret message and hide it invisibly inside an image.**

A complete, professional academic project combining **PBKDF2-HMAC-SHA256** password-based key derivation, **Fernet** symmetric encryption, and **LSB image steganography** — all in a modern Python desktop application.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Password-based encryption** | PBKDF2-HMAC-SHA256 (390,000 iterations) + Fernet AES-128-CBC |
| **LSB Steganography** | 1-bit LSB per R/G/B channel, imperceptible to human eye |
| **Structured binary payload** | Magic header + version + length + salt + encrypted token |
| **Image quality analysis** | MSE, PSNR, SSIM via scikit-image |
| **Performance benchmarks** | Timing graphs across multiple message sizes |
| **Plain vs Encrypted LSB** | Academic comparison table |
| **100% offline** | No network calls — all processing is local |

---

## 📋 Requirements

- Python 3.11+
- See `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python main.py
```

### Hide a message

1. Open the application → **Hide Message**
2. Enter your secret plain-text message
3. Select a cover image (PNG, JPG, BMP)
4. Enter a strong password and confirm it
5. Click **ENCRYPT & HIDE**
6. Save the output `stego.png`

### Extract a message

1. Go to **Extract Message**
2. Select the `stego.png` file
3. Enter the same password
4. Click **EXTRACT & DECRYPT**
5. The original message appears instantly

---

## 🔬 Cryptographic Design

```
Password + Random 16-byte Salt
          ↓
  PBKDF2-HMAC-SHA256 (390,000 iterations)
          ↓
       32-byte Key
          ↓
        Fernet
          ↓
   Encrypted Token (bytes)
          ↓
Structured Binary Payload (no extra Base64)
          ↓
     LSB Embedding
```

### Payload binary format

```
Offset  Length  Field
  0       4     Magic: "STEG"
  4       1     Version: 0x01
  5       4     Token length (uint32 big-endian)
  9      16     PBKDF2 salt (random, not secret)
 25       N     Fernet encrypted token
```

---

## 🗂 Project Structure

```
secure-steganography/
├── main.py                    Entry point
├── requirements.txt
├── README.md
├── PROJECT_DOCUMENTATION.md
│
├── crypto/
│   └── encryption.py          PBKDF2 + Fernet
│
├── steganography/
│   └── lsb.py                 LSB embed / extract
│
├── utils/
│   ├── constants.py           App-wide settings
│   ├── payload.py             Payload builder / parser
│   └── validation.py          Input validators
│
├── analysis/
│   ├── metrics.py             MSE, PSNR, SSIM
│   └── performance.py         Timing benchmarks
│
├── gui/
│   ├── main_window.py         Root window + navigation
│   ├── hide_view.py           Hide Message screen
│   ├── extract_view.py        Extract Message screen
│   ├── analysis_view.py       Analysis & benchmarks
│   └── about_view.py          About screen
│
├── tests/
│   ├── test_crypto.py
│   ├── test_lsb.py
│   ├── test_payload.py
│   ├── test_metrics.py
│   └── test_workflow.py       End-to-end tests
│
├── assets/sample_images/
└── results/
```

---

## 🧪 Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## 🔒 Security Notes

- Passwords are **never stored** or logged.
- The 32-byte encryption key is **never displayed**.
- A fresh **random salt** is generated for every Hide operation.
- LSB steganography is **not a substitute for encryption** — it provides obscurity, not confidentiality. The Fernet encryption provides confidentiality.
- This project is intended for **academic and educational purposes**.

---

## 📊 Image Quality

| Metric | Typical LSB Result |
|---|---|
| MSE | < 0.01 |
| PSNR | > 50 dB |
| SSIM | > 0.999 |

LSB changes are imperceptible to the human eye but can be detected by statistical steganalysis tools.

---

## 📚 Technologies

- **Python 3.11**
- **CustomTkinter** — Modern dark-themed GUI
- **Pillow** — Image I/O
- **cryptography** — PBKDF2 + Fernet
- **NumPy** — Vectorised LSB operations
- **Matplotlib** — Performance graphs
- **scikit-image** — SSIM computation
