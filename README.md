# 🎨 Stitch Design Pro (DESIGN.md Generator)

> **Eliminate "AI Slop" & Inconsistent UI in Google Stitch (`stitch.withgoogle.com`).**  
> Generate production-grade, highly cohesive `DESIGN.md` design systems and prompt wrappers powered by **UI/UX Pro Max** design intelligence.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Stitch Compatible](https://img.shields.io/badge/Google%20Stitch-Compatible-orange.svg)](https://stitch.withgoogle.com)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()

---

[Tiếng Việt](#-hướng-dẫn-tiếng-việt) | [English](#-english-guide)

---

## 🇻🇳 Hướng Dẫn Tiếng Việt

### 1. Vấn đề thực tế với Google Stitch
Khi tạo giao diện trên **Google Stitch** ([stitch.withgoogle.com](https://stitch.withgoogle.com)), người dùng thường gặp các vấn đề:
* **Context Drift (Mất tính nhất quán):** Màn hình 1 bo góc `16px` viền tím, màn hình 2 lại tự ý đổi sang bo góc `8px` nút xanh.
* **"AI Slop" (Giao diện phèn):** AI tự động nhồi nhét gradient lòe loẹt, drop-shadow quá đà, viền phát sáng và icon lộn xộn.
* **Không có Design Tokens:** Thiếu hệ thống phân cấp màu (60-30-10), lưới không gian (8pt grid) và tỷ lệ font chữ.

### 2. Giải pháp: `Stitch Design Pro`
Dự án này cung cấp công cụ tự động tạo file **`DESIGN.md`** (Design DNA) chuẩn xác cho Google Stitch, kết hợp với các nguyên tắc từ **UI/UX Pro Max**:
1. **Khóa chặt Design Tokens:** Tự tính toán bảng màu chuẩn 60-30-10, WCAG AA tương phản cao.
2. **Loại bỏ AI Slop (Negative Constraints):** Tự động cấm gradient ngẫu nhiên, cấm trộn icon, cố định chiều cao nút 48px.
3. **Enhanced Prompt Generator:** Tự động gói yêu cầu màn hình vào prompt chuẩn để copy thẳng vào Stitch.
4. **Không phụ thuộc thư viện ngoài:** Chạy mượt mà với 100% thư viện chuẩn của Python 3 (Standard Library).

---

### 3. Cài đặt & Sử dụng nhanh

```bash
# Clone repository
git clone https://github.com/vinhvox/Stitch-design-generator.git
cd Stitch-design-generator

# Cách 1: Chế độ tương tác hỏi-đáp (Interactive Wizard)
python3 generator.py --interactive

# Cách 2: Tạo nhanh bằng lệnh 1 dòng
python3 generator.py "fintech investment crypto wallet" -p "ApexWallet" -o DESIGN.md

# Cách 3: Tạo DESIGN.md kèm PROMPT để copy ngay vào Stitch
python3 generator.py "fitness workout gym tracker" -p "PulseFit" \
  --prompt-for "Màn hình bắt đầu bài tập với bộ đếm giờ và danh sách hiệp tập"
```

---

## 🇬🇧 English Guide

### Overview
**Google Stitch** is an innovative AI canvas, but raw prompt generation often results in inconsistent styles, conflicting color palettes, and generic "AI slop".  

`Stitch Design Pro` bridges this gap by generating a disciplined `DESIGN.md` specification that acts as the **Single Source of Truth (SSOT)** for Stitch's Gemini models.

### Key Features
* 💎 **Strict 60-30-10 Color Balance**: 60% neutral canvas/surface, 30% structural text, 10% purposeful CTA accent.
* 📐 **8pt Spatial Grid & Ergonomics**: Enforces `48px` minimum touch targets and cohesive corner radiuses.
* 🛡️ **Anti-AI Slop Guardrails**: Strict negative constraints against gratuitous glows, heavy drop shadows, and mismatched icons.
* ⚡ **Zero External Dependencies**: Pure Python 3 standard library. Runs anywhere instantly.
* 🧠 **UI/UX Pro Max Integration**: Automatically detects and leverages local `ui-ux-pro-max` design intelligence if installed.

---

### CLI Reference

```bash
usage: generator.py [-h] [-p PROJECT] [--platform {mobile,web}] [-o OUTPUT]
                    [--prompt-for PROMPT_FOR] [--interactive]
                    [query]

positional arguments:
  query                 App description or industry (e.g. 'fintech expense tracker')

options:
  -h, --help            show this help message and exit
  -p, --project PROJECT Project name
  --platform {mobile,web} Target platform (default: mobile)
  -o, --output OUTPUT   Output file path (default: DESIGN.md)
  --prompt-for PROMPT_FOR Also generate an enhanced Stitch prompt for a screen
  --interactive         Run interactive questionnaire wizard
```

---

### Folder Structure
```
stitch-design-generator/
├── generator.py                  # Core CLI & Design System Synthesizer
├── SKILL.md                      # Agent Skill spec (Cursor, Claude Code, Antigravity)
├── templates/
│   ├── DESIGN.md.template        # Base DESIGN.md markdown template
│   └── stitch-prompt.md.template # Prompt wrapper for Stitch
├── examples/
│   ├── fintech-crypto-wallet/    # ApexWallet example & prompt
│   ├── health-fitness-tracker/   # PulseFit example & prompt
│   └── ecommerce-fashion/        # AuraFashion example & prompt
├── LICENSE                       # MIT License
└── README.md                     # Documentation
```

---

### Using as an AI Agent Skill

If you use **Claude Code**, **Cursor**, **Antigravity IDE**, or **Gemini CLI**, you can install this skill directly:

```bash
npx skills add vinhvox/Stitch-design-generator --skill stitch-design-pro
```

---

## 🤝 Contributing
Contributions, industry profiles, and new templates are welcome! Feel free to open an Issue or submit a Pull Request.

## 📄 License
This project is open-source under the [MIT License](LICENSE).
