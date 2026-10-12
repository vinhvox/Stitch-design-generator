#!/usr/bin/env python3
"""
Stitch Design Pro — Taste & Aesthetics Engine
============================================
Generates production-grade, aesthetically sophisticated DESIGN.md files and
tailored prompts for Google Stitch (stitch.withgoogle.com).

Explicitly engineered to eliminate:
- "AI Boxy Syndrome" (putting everything in boring 1px bordered rectangular boxes)
- Clunky heavy black buttons
- Sterile, clinical, uninspired admin-like interfaces

Injects human-crafted design taste:
- Editorial warmth, fluid whitespace, borderless typography
- Elegant color temperatures (Warm Paper, Deep Obsidian, Nordic Zen)
- Floating pill ergonomics and subtle hairline dividers

Zero third-party dependencies required (Standard Python 3 only).
"""

import os
import sys
import json
import argparse
import subprocess
from typing import Dict, Any, Optional

UI_UX_PRO_MAX_SCRIPT = os.path.expanduser("~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py")

# ==============================================================================
# TASTE & AESTHETIC ENGINES (Design Personas)
# ==============================================================================
TASTE_PERSONAS: Dict[str, Dict[str, Any]] = {
    "editorial_warmth": {
        "name": "Editorial Warmth (Paper & Craft)",
        "tagline": "Ấm áp, Thủ công, Tạp chí nghệ thuật như Apple Books, Craft Docs, Kinfolk",
        "bg_canvas": "#FAF8F5",       # Warm Paper / Cream
        "bg_surface": "#FFFFFF",      # Crisp White surface
        "border_subtle": "#EFECE6",   # Organic warm hairline border (0.5px-1px)
        "text_primary": "#1C1917",    # Warm Charcoal Velvet
        "text_secondary": "#78716C",  # Warm Stone Grey
        "brand_primary": "#B45309",   # Rich Warm Amber / Terracotta
        "brand_primary_hover": "#92400E",
        "status_success": "#15803D",
        "status_error": "#BE123C",
        "font_display": "Newsreader / Playfair Display / Serif Expressive",
        "font_body": "Inter / SF Pro Text, relaxed line-height (1.6)",
        "radius_card": "16px",
        "radius_button": "9999px",    # Floating Pill
        "button_height": "46px",
        "icon_style": "Lucide / Feather, 18px, delicate 1.5px stroke",
        "layout_philosophy": "Borderless & Whitespace-first. NO isolated bordered card boxes. Content flows organically with generous breathing room and hairline dividers.",
        "anti_slop_rules": [
            "CẤM đóng khung từng dòng danh sách tài liệu thành các hộp chữ nhật viền xám.",
            "CẤM nút bấm đen sì chiếm 100% chiều ngang màn hình. Hãy dùng Floating Pill hoặc Capsule Button thanh thoát.",
            "CẤM nhồi nhét thông số kỹ thuật (MB, format, encryption) thành các badge dày đặc.",
            "BẮT BUỘC dùng nền kem giấy tự nhiên, phân cấp chữ rõ rệt (tiêu đề lớn phóng khoáng, chú thích nhỏ tinh tế)."
        ]
    },
    "linear_obsidian": {
        "name": "Linear Obsidian (Sleek Dark Pro)",
        "tagline": "Đen sâu huyền bí, Tinh xảo, Tối giản công nghệ như Linear, Raycast, Superhuman",
        "bg_canvas": "#090A0F",       # Deep Obsidian
        "bg_surface": "#12141A",      # Smoky Slate Surface
        "border_subtle": "#1F232D",   # Hairline subtle metallic border
        "text_primary": "#F1F5F9",    # Pristine Soft White
        "text_secondary": "#94A3B8",  # Muted Slate
        "brand_primary": "#6366F1",   # Electric Indigo / Violet
        "brand_primary_hover": "#4F46E5",
        "status_success": "#10B981",
        "status_error": "#F43F5E",
        "font_display": "Inter Display / SF Pro Display, tight letter-spacing (-0.02em)",
        "font_body": "Inter / Geist, high legibility",
        "radius_card": "12px",
        "radius_button": "8px",
        "button_height": "44px",
        "icon_style": "Lucide, 18px, precision 1.75px stroke",
        "layout_philosophy": "Precision high-density with micro-accents. Grouped inset surfaces with hairline borders, subtle glow only on active indicators.",
        "anti_slop_rules": [
            "CẤM background đen thuần thô thiển; phải có độ sâu giữa canvas (#090A0F) và surface (#12141A).",
            "CẤM nút bấm to bản thô ráp; dùng nút kích thước vừa phải với viền phát quang siêu nhẹ.",
            "CẤM icon màu sắc sặc sỡ hỗn loạn; đồng nhất icon đơn sắc thanh mảnh."
        ]
    },
    "nordic_zen": {
        "name": "Nordic Zen (Pure Minimalism)",
        "tagline": "Tối giản thanh khiết, Tĩnh lặng, Cực nhiều khoảng thở như Muji, Nothing OS",
        "bg_canvas": "#FFFFFF",       # Pure Canvas
        "bg_surface": "#F6F6F7",      # Soft Chalk Gray
        "border_subtle": "#E5E5E7",   # Whisper Gray border
        "text_primary": "#111111",    # Pure Pitch Black
        "text_secondary": "#6E6E73",  # Apple-grade Muted Text
        "brand_primary": "#2D3139",   # Deep Graphite Charcoal
        "brand_primary_hover": "#1A1C20",
        "status_success": "#2E7D32",
        "status_error": "#D32F2F",
        "font_display": "Inter / Neue Haas Grotesk, geometric & confident",
        "font_body": "Inter, clean 14px",
        "radius_card": "14px",
        "radius_button": "9999px",    # Clean Pill
        "button_height": "48px",
        "icon_style": "Feather outline, 20px, 1.5px clean stroke",
        "layout_philosophy": "Whitespaces are the primary design element. Asymmetrical layout, zero redundant decoration, zero drop shadows.",
        "anti_slop_rules": [
            "CẤM hoàn toàn gradient hoặc drop shadow.",
            "CẤM các bảng điều khiển đóng hộp kiểu admin. Dùng typography và khoảng cách 32px-48px để phân vùng.",
            "CẤM quá 2 cấp độ màu trên một màn hình."
        ]
    },
    "modern_luxury": {
        "name": "Modern Luxury & Editorial",
        "tagline": "Sang trọng, Đẳng cấp thương gia, Tạp chí thời trang quốc tế",
        "bg_canvas": "#FDFBF7",       # Alabaster White
        "bg_surface": "#FFFFFF",
        "border_subtle": "#ECE6DA",   # Champagne hairline
        "text_primary": "#18181B",    # Deep Onyx
        "text_secondary": "#71717A",  # Warm Zinc
        "brand_primary": "#047857",   # Deep Forest Emerald / British Racing Green
        "brand_primary_hover": "#065F46",
        "status_success": "#047857",
        "status_error": "#991B1B",
        "font_display": "Playfair Display / Cormorant Garamond, editorial serif",
        "font_body": "Plus Jakarta Sans / Inter",
        "radius_card": "12px",
        "radius_button": "6px",
        "button_height": "48px",
        "icon_style": "Lucide minimal, 20px, 1.5px stroke",
        "layout_philosophy": "Bespoke grid, editorial hierarchy, expansive photography & clean negative space.",
        "anti_slop_rules": [
            "CẤM dùng font sans-serif cho cả tiêu đề nếu muốn thể hiện tính đẳng cấp.",
            "CẤM viền đen dày hoặc nút bấm thô thiển.",
            "BẮT BUỘC giữ tỷ lệ tương phản cao cấp và khoảng cách giữa các phần tử tối thiểu 24px."
        ]
    },
    "modern_consumer": {
        "name": "Modern Consumer Fluid (Airbnb / Notion Style)",
        "tagline": "Thân thiện, Mềm mại, Trẻ trung, Trực quan và Dễ chịu",
        "bg_canvas": "#FFFFFF",
        "bg_surface": "#F8FAFC",
        "border_subtle": "#F1F5F9",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "brand_primary": "#0D9488",   # Modern Teal / Cyan
        "brand_primary_hover": "#0F766E",
        "status_success": "#16A34A",
        "status_error": "#E11D48",
        "font_display": "Plus Jakarta Sans, bold, rounded tracking",
        "font_body": "Inter / Roboto, 14px",
        "radius_card": "20px",        # Generous rounded corners
        "radius_button": "9999px",    # Capsule Button
        "button_height": "50px",
        "icon_style": "Solar / Lucide rounded outline, 22px",
        "layout_philosophy": "Card-less grouped insets, soft organic touch points, seamless thumb navigation.",
        "anti_slop_rules": [
            "CẤM góc bo sắc nhọn (<12px).",
            "CẤM các bảng dữ liệu dạng form bảng tính.",
            "Ưu tiên floating action bars và micro-interactions."
        ]
    }
}


def query_ui_ux_pro_max(query: str, project_name: str) -> Optional[Dict[str, Any]]:
    """Tries to query local UI/UX Pro Max search engine if available."""
    if not os.path.exists(UI_UX_PRO_MAX_SCRIPT):
        return None

    try:
        cmd = [
            sys.executable,
            UI_UX_PRO_MAX_SCRIPT,
            query,
            "--design-system",
            "-p", project_name
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and "TARGET:" in res.stdout:
            return parse_pro_max_output(res.stdout)
    except Exception:
        pass
    return None


def parse_pro_max_output(stdout: str) -> Dict[str, Any]:
    """Extracts tokens from UI/UX Pro Max CLI text output."""
    profile = dict(TASTE_PERSONAS["editorial_warmth"])

    for line in stdout.splitlines():
        line = line.strip()
        clean_line = line.replace("│", "").replace("║", "").replace("┌", "").replace("└", "").replace("├", "").strip()
        
        if "Primary:" in clean_line and "(--color-primary)" in clean_line:
            parts = clean_line.split()
            for idx, p in enumerate(parts):
                if p == "Primary:" and idx + 1 < len(parts):
                    profile["brand_primary"] = parts[idx + 1]
                    profile["brand_primary_hover"] = parts[idx + 1]
        elif "Background:" in clean_line and "(--color-background)" in clean_line:
            parts = clean_line.split()
            for idx, p in enumerate(parts):
                if p == "Background:" and idx + 1 < len(parts):
                    profile["bg_canvas"] = parts[idx + 1]
        elif "Card:" in clean_line and "(--color-card)" in clean_line:
            parts = clean_line.split()
            for idx, p in enumerate(parts):
                if p == "Card:" and idx + 1 < len(parts):
                    profile["bg_surface"] = parts[idx + 1]
        elif "Foreground:" in clean_line and "(--color-foreground)" in clean_line:
            parts = clean_line.split()
            for idx, p in enumerate(parts):
                if p == "Foreground:" and idx + 1 < len(parts):
                    profile["text_primary"] = parts[idx + 1]
        elif "Border:" in clean_line and "(--color-border)" in clean_line:
            parts = clean_line.split()
            for idx, p in enumerate(parts):
                if p == "Border:" and idx + 1 < len(parts):
                    profile["border_subtle"] = parts[idx + 1]

    return profile


def generate_design_md(
    project_name: str,
    query: str,
    taste_key: str = "editorial_warmth",
    layout_mode: str = "borderless",
    button_mode: str = "pill",
    color_override: Optional[Dict[str, str]] = None,
    platform: str = "mobile"
) -> str:
    """Generates an aesthetically rich, anti-boxy DESIGN.md for Google Stitch."""
    taste = TASTE_PERSONAS.get(taste_key, TASTE_PERSONAS["editorial_warmth"]).copy()

    # Apply overrides if provided
    if color_override:
        taste.update({k: v for k, v in color_override.items() if v})

    if button_mode == "pill":
        taste["radius_button"] = "9999px"
    elif button_mode == "soft":
        taste["radius_button"] = "12px"
    elif button_mode == "minimal":
        taste["radius_button"] = "6px"

    is_mobile = "mobile" in platform.lower()
    screen_padding = "20px horizontal, 24px vertical" if is_mobile else "32px horizontal, 40px vertical"
    container_max = "100% (Fluid Mobile Viewport)" if is_mobile else "1280px (Centered Editorial Canvas)"

    rules_markdown = "\n".join([f"- 🛡️ {r}" for r in taste.get("anti_slop_rules", [])])

    md = f"""# {project_name} — High-Aesthetic Design System Specification (DESIGN.md)
<!-- Generated by Stitch Design Pro (Taste Engine: {taste['name']}) -->
<!-- Source of Truth for Google Stitch AI Canvas (stitch.withgoogle.com) -->

## 1. Brand Identity & Aesthetic Soul
- **Project Name**: {project_name}
- **Design Persona**: {taste['name']}
- **Aesthetic Direction**: {taste['tagline']}
- **Target Platform**: {platform.upper()} ({container_max})
- **Core Philosophy**: **Anti-Boxy, Content-First, Editorial Fluidity.** No administrative tables, no generic cards-in-cards.

---

## 2. Refined Color Atmosphere (WCAG AA Compliant)
| Token Name | Hex Value | Atmospheric Purpose |
| :--- | :--- | :--- |
| `--bg-canvas` | `{taste['bg_canvas']}` | **60% Base**: Organically warm, anti-glare reading canvas |
| `--bg-surface` | `{taste['bg_surface']}` | Surface: Elevated sheets, modal dialogs, search pills |
| `--border-subtle` | `{taste['border_subtle']}` | **0.5px - 1px Hairline**: Barely noticeable separation divider |
| `--text-primary` | `{taste['text_primary']}` | Deep, velvety, high-legibility heading & reading copy |
| `--text-secondary` | `{taste['text_secondary']}` | **30% Structural**: Subtle metadata, dates, secondary labels |
| `--brand-primary` | `{taste['brand_primary']}` | **10% Signature Accent**: Floating pill CTA & active state only |
| `--brand-primary-hover` | `{taste['brand_primary_hover']}` | Pressed / interaction state |
| `--status-success` | `{taste['status_success']}` | Refined harmonic indicator (non-alarmist) |
| `--status-error` | `{taste['status_error']}` | Gentle destructive state |

---

## 3. Typographic Elegance & Hierarchy
- **Display & Headline Font**: `{taste['font_display']}`
- **Body & Functional Font**: `{taste['font_body']}`
- **Scale Hierarchy**:
  - **Hero / Screen Title**: `28px` | Weight: `700` | Line Height: `36px` | Tracking: `-0.02em`
  - **Section Headline**: `20px` | Weight: `600` | Line Height: `28px`
  - **Body / Primary Copy**: `15px` | Weight: `400` | Line Height: `24px` (Generous reading room)
  - **Caption & Micro-Data**: `12px` | Weight: `500` | Line Height: `16px` | Tracking: `+0.01em`

---

## 4. Anti-Boxy Spatial Layout & Ergonomics
- **Layout Philosophy**: `{taste['layout_philosophy']}`
- **Screen Padding**: `{screen_padding}`
- **List Items (CRITICAL)**:
  - ❌ **DO NOT enclose items inside bordered rectangular cards.**
  - ✅ **Use Borderless List Items**: Items sit directly on the canvas, separated by 16px vertical padding and a subtle `0.5px` hairline divider (`var(--border-subtle)`).
- **Interactive Buttons**:
  - Style: `{taste['radius_button']}` ({button_mode.upper()} style)
  - Height: `{taste['button_height']}` (Touch ergonomic standard)
  - Layout Rule: **Never stretch heavy black buttons 100% width across the bottom.** Use Floating Pill Actions (width: auto or inset with margins).
- **Navigation**:
  - Bottom Bar: Floating frosted/tinted capsule or minimal text-dock with 3-4 items max.
  - Icons: `{taste['icon_style']}`.

---

## 5. Strict Negative Constraints (Zero AI-Slop Directives)
{rules_markdown}
- ❌ **CẤM Hội chứng đóng hộp (Boxy Syndrome)**: Không nhét tất cả thông tin vào các thẻ card viền xám xếp chồng.
- ❌ **CẤM Nút khối đen nặng nề**: Tuyệt đối không dùng nút chữ nhật đen đặc choán hết màn hình.
- ❌ **CẤM Gradient sặc sỡ & Drop Shadow đen đặc**: Giữ độ phẳng tinh tế, chiều sâu thể hiện qua khoảng cách màu và hairline.
"""
    return md


def generate_stitch_prompt(project_name: str, screen_description: str, design_md_content: str) -> str:
    """Generates an enhanced prompt specifically commanding Stitch to avoid boxiness."""
    prompt = f"""You are a World-Class Principal Product Designer & Art Director building "{project_name}".
Create the following screen: "{screen_description}".

CRITICAL AESTHETIC DIRECTIVES (STRICT ZERO-AI-SLOP):
1. **ANTI-BOXY ARCHITECTURE**:
   - DO NOT create rectangular card boxes inside card boxes.
   - DO NOT make it look like an admin dashboard or spreadsheet.
   - Use a borderless, editorial layout inspired by Apple Books, Craft Docs, and Kinfolk: clean whitespace, organic typography flow, and hairline dividers.
2. **FLOATING PILL ERGONOMICS**:
   - DO NOT create heavy, full-width black rectangular buttons at the bottom.
   - Use refined Floating Action Pills or elegant text buttons with generous padding.
3. **COLOR & TYPOGRAPHY DISCIPLINE**:
   - Strictly adhere to the tokens defined in DESIGN.md below.
   - Maintain the warm, sophisticated color temperature.

DESIGN.md REFERENCE:
```markdown
{design_md_content.strip()}
```
"""
    return prompt


# ==============================================================================
# DEEP INTERACTIVE CONSULTATION WIZARD
# ==============================================================================
def interactive_mode():
    """Runs a deep, multi-dimensional design consultation wizard."""
    print("\n" + "═" * 72)
    print(" 🎨  STITCH DESIGN PRO — INTERACTIVE ART DIRECTION CONSULTATION")
    print("     (Tạo DESIGN.md có gu, thanh thoát, xóa bỏ hoàn toàn chất AI)")
    print("═" * 72)

    # 1. Project Info
    print("\n[Bước 1/6] 📱 THÔNG TIN SẢN PHẨM & NGHIỆP VỤ")
    project_name = input("  ▸ Tên dự án (Project Name) [My App]: ").strip() or "My App"
    query = input(f"  ▸ Mô tả cốt lõi của '{project_name}' (ví dụ: Tool đọc file PDF nhanh, App thiền, Quản lý tài chính cá nhân): ").strip()
    if not query:
        query = "Minimalist Tool Application"

    # 2. Aesthetic Taste Engine (Gu thẩm mỹ)
    print("\n[Bước 2/6] 🎭 GU THẨM MỸ & CÁ TÍNH HÌNH ẢNH (Aesthetic Persona)")
    print("  Chọn 1 phong cách thiết kế định hình 'linh hồn' của app:")
    personas_keys = list(TASTE_PERSONAS.keys())
    for idx, key in enumerate(personas_keys, 1):
        item = TASTE_PERSONAS[key]
        print(f"    [{idx}] {item['name']}")
        print(f"        └─ {item['tagline']}")

    choice_taste = input(f"  ▸ Chọn phong cách [1-{len(personas_keys)}] (Mặc định 1 - Editorial Warmth): ").strip()
    try:
        taste_idx = int(choice_taste) - 1
        if 0 <= taste_idx < len(personas_keys):
            selected_taste_key = personas_keys[taste_idx]
        else:
            selected_taste_key = "editorial_warmth"
    except ValueError:
        selected_taste_key = "editorial_warmth"

    selected_persona = TASTE_PERSONAS[selected_taste_key]
    print(f"  👉 Đã chọn: {selected_persona['name']}")

    # 3. Layout Philosophy (Bố cục chống đóng hộp)
    print("\n[Bước 3/6] 📐 TRIẾT LÝ BỐ CỤC (Chống bệnh đóng hộp AI)")
    print("  [1] 🌊 Borderless & Fluid (Khuyên dùng): Không đóng khung từng item, dùng khoảng trắng & đường kẻ hairline siêu mảnh.")
    print("  [2] 📱 Soft Grouped Inset: Khối bo góc lớn mềm mại (18px-24px), thanh thoát chuẩn iOS Human Interface.")
    print("  [3] 🎈 Floating Canvas: Thanh dock & pill nổi, bố cục mở phóng khoáng.")
    choice_layout = input("  ▸ Chọn triết lý bố cục [1-3] (Mặc định 1): ").strip()
    layout_mode = "borderless" if choice_layout != "2" and choice_layout != "3" else ("grouped" if choice_layout == "2" else "floating")

    # 4. Color Atmosphere (Bầu không khí màu sắc)
    print("\n[Bước 4/6] 🖌️ NHIỆT ĐỘ MÀU SẮC (Color Atmosphere)")
    print(f"  [1] Giữ nguyên palette chuẩn của phong cách đã chọn ({selected_persona['bg_canvas']} / Accent: {selected_persona['brand_primary']})")
    print("  [2] Tông Giấy ngà ấm áp (Warm Cream #FAF8F5 / Hổ phách #B45309) - Rất dịu mắt cho việc đọc")
    print("  [3] Tông Obsidian Tối sang trọng (Deep Dark #090A0F / Tím điện #6366F1)")
    print("  [4] Tự nhập mã màu Accent tùy chỉnh (Custom Hex Code)")

    choice_color = input("  ▸ Chọn bầu không khí màu [1-4] (Mặc định 1): ").strip()
    color_override = {}
    if choice_color == "2":
        color_override = {
            "bg_canvas": "#FAF8F5",
            "bg_surface": "#FFFFFF",
            "text_primary": "#1C1917",
            "brand_primary": "#B45309"
        }
    elif choice_color == "3":
        color_override = {
            "bg_canvas": "#090A0F",
            "bg_surface": "#12141A",
            "text_primary": "#F1F5F9",
            "brand_primary": "#6366F1"
        }
    elif choice_color == "4":
        custom_accent = input("    ▸ Nhập mã Hex màu Accent bạn muốn (ví dụ #059669, #EA580C): ").strip()
        if custom_accent.startswith("#") and len(custom_accent) in [4, 7]:
            color_override = {"brand_primary": custom_accent, "brand_primary_hover": custom_accent}

    # 5. Button & Micro-Interactions (Phong cách nút bấm)
    print("\n[Bước 5/6] 🔘 PHONG CÁCH NÚT BẤM (CTA) & TƯƠNG TÁC")
    print("  [1] 💊 Floating Pill / Capsule (Nút viên nhộng bo tròn 9999px mềm mại, không bao giờ thô)")
    print("  [2] 🏷️  Soft Rounded (Bo góc 12px vừa phải, kích thước gọn gàng)")
    print("  [3] ✍️  Minimal Text Action (Tối giản hoàn toàn, ưu tiên text link & icon)")
    choice_btn = input("  ▸ Chọn phong cách nút [1-3] (Mặc định 1): ").strip()
    btn_mode = "pill" if choice_btn != "2" and choice_btn != "3" else ("soft" if choice_btn == "2" else "minimal")

    # 6. Target Platform & Output
    print("\n[Bước 6/6] 🎯 NỀN TẢNG & XUẤT FILE")
    platform = input("  ▸ Nền tảng (mobile / web) [mobile]: ").strip() or "mobile"
    output_file = input("  ▸ Tên file xuất ra [DESIGN.md]: ").strip() or "DESIGN.md"
    prompt_for_screen = input("  ▸ Bạn muốn tạo kèm prompt cho màn hình cụ thể nào không? (Để trống nếu không cần): ").strip()

    print(f"\n⚙️  Đang tổng hợp Design System có gu nghệ thuật cho '{project_name}'...")
    content = generate_design_md(
        project_name=project_name,
        query=query,
        taste_key=selected_taste_key,
        layout_mode=layout_mode,
        button_mode=btn_mode,
        color_override=color_override,
        platform=platform
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ ĐÃ TẠO THÀNH CÔNG: '{output_file}'")

    if prompt_for_screen:
        output_dir = os.path.dirname(output_file) or "."
        base_name = os.path.basename(output_file)
        prompt_output = os.path.join(output_dir, f"PROMPT_{base_name}")
        prompt_content = generate_stitch_prompt(project_name, prompt_for_screen, content)
        with open(prompt_output, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        print(f"📋 ĐÃ TẠO PROMPT TƯƠNG ỨNG: '{prompt_output}'")

    print("\n" + "═" * 72)
    print("💡 MẸO SỬ DỤNG TRÊN GOOGLE STITCH:")
    print(" 1. Copy toàn bộ nội dung file DESIGN.md nạp vào Stitch canvas.")
    print(" 2. Dùng file PROMPT vừa tạo dán vào ô chat của Stitch để sinh từng màn hình.")
    print(" 3. Stitch sẽ tuân thủ tuyệt đối quy tắc 'Không đóng hộp', tạo ra giao diện mềm mại, có gu!")
    print("═" * 72 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Stitch Design Pro — Generate High-Aesthetic DESIGN.md for Google Stitch"
    )
    parser.add_argument("query", nargs="?", default="", help="App description or industry")
    parser.add_argument("-p", "--project", default="App Project", help="Project name")
    parser.add_argument("--platform", default="mobile", choices=["mobile", "web"], help="Target platform")
    parser.add_argument("--taste", default="editorial_warmth", choices=list(TASTE_PERSONAS.keys()), help="Aesthetic taste engine")
    parser.add_argument("-o", "--output", default="DESIGN.md", help="Output file path")
    parser.add_argument("--prompt-for", help="Also generate an enhanced Stitch prompt for a specific screen")
    parser.add_argument("--interactive", action="store_true", help="Run interactive consultation wizard")

    args = parser.parse_args()

    if args.interactive or not args.query:
        interactive_mode()
        return

    content = generate_design_md(
        project_name=args.project,
        query=args.query,
        taste_key=args.taste,
        platform=args.platform
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✨ Successfully generated '{args.output}' for '{args.project}' ({args.platform})")

    if args.prompt_for:
        prompt_content = generate_stitch_prompt(args.project, args.prompt_for, content)
        output_dir = os.path.dirname(args.output) or "."
        base_name = os.path.basename(args.output)
        prompt_output = os.path.join(output_dir, f"PROMPT_{base_name}")
        with open(prompt_output, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        print(f"📋 Generated Stitch Copy-Paste Prompt: '{prompt_output}'")


if __name__ == "__main__":
    main()
