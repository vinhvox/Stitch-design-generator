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

### 2. Giải pháp: `Stitch Design Pro` (Phiên bản Taste & Aesthetics Engine)
Dự án này cung cấp công cụ tự động tạo file **`DESIGN.md`** (Design DNA) chuẩn xác cho Google Stitch, giải quyết triệt để vấn đề "thô cứng" và "mùi AI":
1. **5 Động cơ Gu thẩm mỹ (Taste Engines):**
   * 📖 **Editorial Warmth (Paper & Craft):** Phong cách ấm áp, nền giấy ngà, tạp chí cao cấp như Apple Books, Craft Docs, Readwise.
   * 🖤 **Linear Obsidian (Sleek Dark):** Đen sâu huyền bí, tinh xảo, tối giản công nghệ như Linear, Raycast, Superhuman.
   * 🌿 **Nordic Zen (Pure Minimalism):** Tối giản thanh khiết, ngập tràn khoảng thở như Muji, Nothing OS.
   * 💎 **Modern Luxury & Editorial:** Sang trọng, font có chân quý phái, đẳng cấp thương gia.
   * ⚡ **Modern Consumer Fluid:** Trẻ trung, mềm mại, trực quan như Airbnb, Notion.
2. **Xóa sổ "Bệnh đóng hộp" (Anti-Boxy Directives):**
   * ❌ CẤM nhồi nhét mọi thứ vào các ô chữ nhật viền xám xếp chồng kiểu bảng tính Excel.
   * ❌ CẤM các nút bấm đen sì chiếm 100% chiều ngang màn hình.
   * ✅ BẮT BUỘC dùng **Borderless List Items** (không viền, khoảng trắng tự nhiên, hairline divider 0.5px) và **Floating Action Pills**.
3. **Khảo sát thích ứng theo lĩnh vực (Adaptive Dynamic Branching):** Các câu hỏi tự động thay đổi thông minh theo từng ngành (ví dụ: Tool tính toán sẽ hỏi về trải nghiệm bàn phím, app đọc sách sẽ hỏi về chất giấy và thanh chú thích).
4. **Nhập yêu cầu đặc biệt tùy ý (Free-form Custom Directives):** Cho phép bạn tự do viết bất kỳ mong muốn nào ở bước cuối cùng (ví dụ: *"Nút AC có màu cam", "Font số Monospace", "Thanh trượt góc trên"*), hệ thống sẽ nhúng thẳng vào `DESIGN.md` và các prompt cho Stitch!
5. **Tự động lưu vào folder dự án riêng biệt (`projects/<tên-dự-án>/`):** Không bao giờ ghi đè lên các dự án cũ.
6. **Dashboard xem trước trực quan (`preview.html`):** Double-click mở file HTML trong trình duyệt để thử màu sắc, xem component thực tế và sao chép prompt từng màn hình bằng 1 cú click chuột!
7. **Cầu nối Design-to-Code:** Tự động xuất kèm mã nguồn `tokens.css` (cho Web / Tailwind) và `ThemeTokens.kt` (cho Android Jetpack Compose).
8. **Không phụ thuộc thư viện ngoài:** Chạy mượt mà với 100% thư viện chuẩn của Python 3 (Standard Library).

---

### 3. Cài đặt & Sử dụng nhanh

```bash
# Clone repository
git clone https://github.com/vinhvox/Stitch-design-generator.git
cd Stitch-design-generator

# Cách 1: Chế độ tương tác hỏi-đáp 7 bước (Khuyên dùng)
python3 generator.py --interactive
# 👉 Tự động tạo trọn bộ sản phẩm trong: projects/<tên-app>/

# Cách 2: Xem danh sách các dự án đã tạo
python3 generator.py --list

# Cách 3: Tạo nhanh bằng lệnh 1 dòng
python3 generator.py "fintech crypto wallet" -p "ApexWallet"
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
├── generator.py                  # Core CLI & Art Direction Engine
├── SKILL.md                      # Agent Skill spec (Cursor, Claude Code, Antigravity)
├── templates/
│   ├── DESIGN.md.template        # Base DESIGN.md markdown template
│   └── stitch-prompt.md.template # Prompt wrapper for Stitch
├── projects/                     # Generated projects (Dedicated folder per project)
│   └── calculator/               # Example project bundle
│       ├── DESIGN.md             # Project Design DNA (Tokens & Rules)
│       ├── STITCH_PROMPTS.md     # Multi-screen prompt suite (Concise + Full)
│       ├── preview.html          # Interactive Web Dashboard & 1-Click Prompt Copy
│       ├── tokens.css            # CSS Variables for Web / Tailwind
│       └── CalculatorTokens.kt   # Jetpack Compose Color & Shape Tokens
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
