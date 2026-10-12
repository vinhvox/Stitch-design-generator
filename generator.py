#!/usr/bin/env python3
"""
Stitch Design Pro — Adaptive Art Direction Consultation Engine
=============================================================
Generates production-grade, aesthetically sophisticated DESIGN.md files,
visual preview.html dashboards, code design tokens (CSS & Kotlin),
and tailored multi-screen prompt suites for Google Stitch (stitch.withgoogle.com).

Features:
- Dynamic Branching: Questions adapt contextually based on the user's domain and taste.
- Free-form Custom Directives: User can inject specific custom requirements & guardrails.
- Anti-Boxy Directives: Eliminates rigid rectangular cards and heavy black buttons.
- Full Design-to-Code Bundle: DESIGN.md + STITCH_PROMPTS.md + preview.html + tokens.css + Tokens.kt.

Zero third-party dependencies required (Standard Python 3 only).
"""

import os
import sys
import re
import json
import argparse
import subprocess
import unicodedata
from typing import Dict, Any, Optional, List

# ANSI formatting helpers for terminal polish
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
RESET = "\033[0m"

UI_UX_PRO_MAX_SCRIPT = os.path.expanduser("~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py")


def slugify(text: str) -> str:
    """Converts a project name into a clean, safe directory slug."""
    norm = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', norm).strip('-').lower()
    return slug or "my-project"


def pascal_case(text: str) -> str:
    """Converts text into PascalCase (e.g. 'paperflow-pdf' -> 'PaperflowPdf')."""
    words = re.findall(r'[a-zA-Z0-9]+', text)
    return "".join(w.capitalize() for w in words) or "AppTheme"


# ==============================================================================
# TASTE & AESTHETIC ENGINES (Design Personas)
# ==============================================================================
TASTE_PERSONAS: Dict[str, Dict[str, Any]] = {
    "editorial_warmth": {
        "name": "Editorial Warmth (Paper & Craft)",
        "tagline": "Ấm áp, Thủ công, Tạp chí nghệ thuật như Apple Books, Craft Docs, Kinfolk",
        "description": "Nền giấy kem ngà tự nhiên, chữ màu than chì nhung êm ái, điểm nhấn hổ phách/đất nung. Loại bỏ ánh sáng chói, tôn vinh con chữ và chống mỏi mắt.",
        "best_for": "App đọc sách/PDF, ghi chú, nhật ký cá nhân, học tập, lifestyle, nội dung sáng tạo.",
        "analogues": "Apple Books, Craft Docs, Readwise Reader, Tạp chí Kinfolk",
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
        "description": "Nền đen tuyền sâu thẳm (OLED), bề mặt xám khói, viền kim loại siêu mảnh (0.5px), điểm nhấn tím điện (electric indigo) hoặc cyan sắc sảo.",
        "best_for": "Dev tools, công cụ năng suất cao (productivity), quản trị dự án pro, app crypto/fintech cao cấp.",
        "analogues": "Linear, Raycast, Arc Browser, Superhuman, Vercel",
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
        "font_body": "Geist / Inter, high legibility",
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
        "description": "Nền trắng tinh khôi, bố cục bất đối xứng, không bóng đổ hay gradient cầu kỳ, dùng khoảng trống để định hình nội dung.",
        "best_for": "App thiền định, habit tracker, todo list tối giản, chăm sóc sức khỏe tinh thần, đồng hồ/thời gian.",
        "analogues": "Muji, Nothing OS, Teenage Engineering, Dieter Rams (Braun)",
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
        "description": "Tiêu đề dùng font có chân (Serif) kiêu sa, nền be ngà, điểm nhấn xanh ngọc lục bảo (British racing green) hoặc vàng champagne.",
        "best_for": "Thương mại điện tử cao cấp, bất động sản, đầu tư chứng khoán cao cấp, tạp chí thời trang.",
        "analogues": "Rolex app, Bloomberg Markets, Tạp chí Vogue, The New York Times",
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
        "tagline": "Thân thiện, Mềm mại, Trẻ trung, Trực quan và Dễ gần",
        "description": "Bo góc lớn hào phóng (16-24px), thanh điều hướng dạng viên nhộng, màu sắc tươi sáng hiện đại (teal, indigo), rất dễ gần.",
        "best_for": "Mạng xã hội, app đặt xe, du lịch, ẩm thực, ứng dụng tiêu dùng hàng ngày, cộng đồng.",
        "analogues": "Airbnb, Notion, Spotify, Duolingo",
        "bg_canvas": "#FFFFFF",
        "bg_surface": "#F8FAFC",
        "border_subtle": "#E2E8F0",
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


def build_taste_profile(
    taste_key: str,
    color_override: Optional[Dict[str, str]] = None,
    button_mode: str = "pill",
    typography_mode: str = "editorial_serif"
) -> Dict[str, Any]:
    """Assembles a completely harmonized taste profile with all token overrides applied."""
    taste = TASTE_PERSONAS.get(taste_key, TASTE_PERSONAS["editorial_warmth"]).copy()

    if color_override:
        taste.update({k: v for k, v in color_override.items() if v})

    if button_mode == "pill":
        taste["radius_button"] = "9999px"
    elif button_mode == "soft":
        taste["radius_button"] = "12px"
    elif button_mode == "minimal":
        taste["radius_button"] = "6px"

    if typography_mode == "modern_sans":
        taste["font_display"] = "Inter / SF Pro Display, geometric & balanced"
        taste["font_body"] = "Inter / SF Pro Text, 15px, line-height 1.5"
    elif typography_mode == "tech_sans":
        taste["font_display"] = "Plus Jakarta Sans / Geist Display, tight letter-spacing (-0.02em)"
        taste["font_body"] = "Geist / Inter, high legibility"

    return taste


# ==============================================================================
# DESIGN.MD GENERATOR
# ==============================================================================
def generate_design_md(
    project_name: str,
    query: str,
    taste: Dict[str, Any],
    layout_mode: str = "borderless",
    platform: str = "mobile",
    target_screens: Optional[List[str]] = None,
    custom_directives: Optional[str] = None
) -> str:
    """Generates an aesthetically rich, anti-boxy DESIGN.md for Google Stitch."""
    is_mobile = "mobile" in platform.lower()
    screen_padding = "20px horizontal, 24px vertical" if is_mobile else "32px horizontal, 40px vertical"
    container_max = "100% (Fluid Mobile Viewport)" if is_mobile else "1280px (Centered Editorial Canvas)"

    rules_markdown = "\n".join([f"- 🛡️ {r}" for r in taste.get("anti_slop_rules", [])])

    screens_section = ""
    if target_screens and len(target_screens) > 0:
        screens_list_md = "\n".join([f"  {idx+1}. **{s.strip()}**" for idx, s in enumerate(target_screens) if s.strip()])
        screens_section = f"""
## 6. Target User Journey & Screens
The AI canvas must maintain 100% token consistency across all following screens:
{screens_list_md}
- Rule: Bottom navigation, card radius, button height, and color tokens must NEVER drift between these screens.
"""

    custom_section = ""
    if custom_directives and custom_directives.strip():
        custom_section = f"""
## 7. Custom Directives & Special Rules (Yêu cầu đặc biệt từ tác giả)
- ⭐ **YÊU CẦU ĐẶC BIỆT**: {custom_directives.strip()}
- **Nguyên tắc thực thi**: Mọi màn hình được sinh ra trên Stitch BẮT BUỘC phải ưu tiên tuyệt đối yêu cầu này trên các quy chuẩn mặc định.
"""

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
  - Style: `{taste['radius_button']}`
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
{screens_section}{custom_section}
"""
    return md


# ==============================================================================
# ENHANCED PROMPTS (Concise + Standalone)
# ==============================================================================
def get_screen_ux_guidance(screen_name: str) -> str:
    """Provides smart layout & ergonomics advice for specific screens."""
    s = screen_name.lower()
    if any(k in s for k in ["calculator", "tính toán", "phím số", "keypad"]):
        return "Bàn phím số rộng rãi công thái học, màn hình hiển thị kết quả số lớn với tracking sắc nét, hàng phím chức năng phụ tinh gọn, không đóng khung từng phím bằng viền xám thô."
    elif any(k in s for k in ["khoa học", "scientific", "trigonometric"]):
        return "Dải phím chuyển Rad/Deg dạng floating pill, các hàm lượng giác sin/cos/tan và log sắp xếp khoa học, các hằng số pi/e có ký hiệu thanh mảnh."
    elif any(k in s for k in ["đổi đơn vị", "unit", "converter", "currency"]):
        return "Bộ chuyển đổi đơn vị 2 chiều mượt mà với segmented control pill, trường nhập số không viền kèm biểu tượng đơn vị thanh lịch."
    elif any(k in s for k in ["thư viện", "library", "danh sách", "list", "books"]):
        return "Danh sách dạng borderless item list, thẻ tệp phẳng đặt trực tiếp trên nền canvas với thumbnail sắc nét và hairline divider 0.5px."
    elif any(k in s for k in ["đọc", "reader", "viewer", "xem"]):
        return "Thanh công cụ ghi chú nổi (Floating Pill) gồm highlight, underline, bookmark; thanh trượt số trang đặt dưới đáy đúng tầm với ngón cái."
    elif any(k in s for k in ["cài đặt", "setting", "preference"]):
        return "Bố cục Soft Grouped Inset với góc bo mềm mại 20px, công tắc switch thanh thoát, mục chọn tông giấy Sepia/OLED trực quan."
    return "Bố cục thoáng đãng, phân cấp thị giác rõ ràng với tiêu đề lớn, khoảng trắng hào phóng và điều hướng bằng thanh pill nổi."


def generate_stitch_prompt_suite(
    project_name: str,
    target_screens: List[str],
    design_md_content: str,
    custom_directives: Optional[str] = None
) -> str:
    """Generates concise 1-click prompts + standalone full prompts."""
    custom_hint = f"\n- CRITICAL AUTHOR DIRECTIVE: {custom_directives.strip()}" if custom_directives and custom_directives.strip() else ""

    sections = []
    for idx, screen in enumerate(target_screens):
        ux_hint = get_screen_ux_guidance(screen)
        sections.append(f"""---

### 🖥️ MÀN HÌNH {idx+1}: {screen.strip()}
> **💡 Gợi ý thiết kế chuyên biệt:** {ux_hint}

#### ⚡ Option A: Prompt Siêu Gọn (Dùng khi đã dán DESIGN.md vào Stitch canvas)
```text
You are a Principal Product Designer building "{project_name}".
Create Screen #{idx+1}: "{screen.strip()}".

STRICT DESIGN SYSTEM INSTRUCTIONS:
- Strictly follow all tokens and rules in the project's DESIGN.md.
- Focus: {ux_hint}
- Anti-Boxy Directive: DO NOT use boxed rectangle cards with 1px borders. Use generous whitespace, borderless typography flow, and hairline dividers.
- Ergonomics: Use floating pill capsule buttons for primary interactions.{custom_hint}
```

#### 📦 Option B: Prompt Độc Lập (Dùng khi mở phiên chat mới trong Stitch)
```text
You are a World-Class Principal Product Designer & Art Director building "{project_name}".
Generate Screen #{idx+1}: "{screen.strip()}".

CRITICAL DIRECTIVES:
1. ANTI-BOXY: No rectangular card boxes inside card boxes. Use borderless fluid typography.
2. FLOATING ERGONOMICS: Floating pill capsule buttons only. Never stretch heavy black buttons across screen.
3. SPECIFICATION: {ux_hint}{custom_hint}

DESIGN.md REFERENCE:
{design_md_content.strip()}
```
""")

    suite = f"""# 📋 Bộ Prompt sinh giao diện Google Stitch cho dự án: {project_name}
<!-- Sử dụng lần lượt các prompt bên dưới trên stitch.withgoogle.com để đảm bảo tính đồng nhất 100% -->

{"".join(sections)}
"""
    return suite


# ==============================================================================
# DESIGN-TO-CODE EXPORTERS (CSS & Kotlin)
# ==============================================================================
def generate_tokens_css(project_name: str, taste: Dict[str, Any]) -> str:
    """Generates standard CSS Custom Properties for web, React, and Tailwind projects."""
    return f"""/* ==============================================================================
   {project_name} — Design Tokens (CSS Variables)
   Generated by Stitch Design Pro
   Compatible with Tailwind CSS, React, Vue, Next.js
   ============================================================================== */

:root {{
  /* Color Tokens */
  --bg-canvas: {taste['bg_canvas']};
  --bg-surface: {taste['bg_surface']};
  --border-subtle: {taste['border_subtle']};
  --text-primary: {taste['text_primary']};
  --text-secondary: {taste['text_secondary']};
  --brand-primary: {taste['brand_primary']};
  --brand-primary-hover: {taste['brand_primary_hover']};
  --status-success: {taste['status_success']};
  --status-error: {taste['status_error']};

  /* Spatial & Geometry */
  --radius-card: {taste['radius_card']};
  --radius-button: {taste['radius_button']};
  --button-height: {taste['button_height']};
  --spacing-screen-x: 20px;
  --spacing-screen-y: 24px;

  /* Typography */
  --font-display: {taste['font_display'].split(',')[0].strip()};
  --font-body: {taste['font_body'].split(',')[0].strip()};
}}
"""


def generate_tokens_kt(project_name: str, taste: Dict[str, Any]) -> str:
    """Generates Kotlin Compose Color & Shape tokens for Android developers."""
    def hex_to_compose(hex_code: str) -> str:
        hex_clean = hex_code.strip().replace("#", "")
        if len(hex_clean) == 6:
            return f"Color(0xFF{hex_clean.upper()})"
        return f"Color(0xFFFFFFFF)"

    pkg_name = slugify(project_name).replace("-", "")
    cls_name = f"{pascal_case(project_name)}Tokens"

    return f"""package com.designsystem.{pkg_name}

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

/**
 * {project_name} Design Tokens for Jetpack Compose.
 * Generated by Stitch Design Pro.
 */
object {cls_name} {{
    // Color Palette
    val BgCanvas = {hex_to_compose(taste['bg_canvas'])}
    val BgSurface = {hex_to_compose(taste['bg_surface'])}
    val BorderSubtle = {hex_to_compose(taste['border_subtle'])}
    val TextPrimary = {hex_to_compose(taste['text_primary'])}
    val TextSecondary = {hex_to_compose(taste['text_secondary'])}
    val BrandPrimary = {hex_to_compose(taste['brand_primary'])}
    val BrandPrimaryHover = {hex_to_compose(taste['brand_primary_hover'])}
    val StatusSuccess = {hex_to_compose(taste['status_success'])}
    val StatusError = {hex_to_compose(taste['status_error'])}

    // Geometry & Touch Ergonomics
    val ButtonHeight = 48.dp
    val ScreenPaddingHorizontal = 20.dp
    val ScreenPaddingVertical = 24.dp
    val CardRadius = 16.dp
    val ButtonRadius = 9999.dp // Pill shape
}}
"""


# ==============================================================================
# VISUAL PREVIEW DASHBOARD (preview.html)
# ==============================================================================
def generate_preview_html(
    project_name: str,
    taste: Dict[str, Any],
    target_screens: List[str],
    custom_directives: Optional[str] = None
) -> str:
    """Generates a standalone, beautiful HTML dashboard to preview design tokens and copy prompts."""
    custom_card_html = ""
    if custom_directives and custom_directives.strip():
        custom_card_html = f"""
        <div style="background: rgba(180, 83, 9, 0.08); border: 1px solid var(--brand-primary); border-radius: var(--radius-card); padding: 18px 20px; margin-bottom: 28px;">
            <div style="font-size: 12px; font-weight: 700; color: var(--brand-primary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">✨ Yêu cầu đặc biệt từ tác giả (Custom Directives)</div>
            <p style="font-size: 14px; color: var(--text-primary);">{custom_directives.strip()}</p>
        </div>
        """

    screens_cards = []
    custom_hint = f"\\n- CRITICAL AUTHOR DIRECTIVE: {custom_directives.strip()}" if custom_directives and custom_directives.strip() else ""

    for idx, screen in enumerate(target_screens):
        hint = get_screen_ux_guidance(screen)
        clean_prompt = f"""You are a Principal Product Designer building "{project_name}".
Create Screen #{idx+1}: "{screen.strip()}".

STRICT DESIGN SYSTEM INSTRUCTIONS:
- Strictly follow all tokens and rules in the project's DESIGN.md.
- Focus: {hint}
- Anti-Boxy Directive: DO NOT use boxed rectangle cards with 1px borders. Use generous whitespace, borderless typography flow, and hairline dividers.
- Ergonomics: Use floating pill capsule buttons for primary interactions.{custom_hint}"""

        escaped_prompt = clean_prompt.replace('"', '&quot;').replace('\n', '&#10;')
        screens_cards.append(f"""
        <div class="screen-card">
            <div class="screen-header">
                <span class="screen-badge">Màn hình #{idx+1}</span>
                <h3 class="screen-title">{screen.strip()}</h3>
            </div>
            <p class="screen-hint">💡 <strong>UX Guidance:</strong> {hint}</p>
            <div class="code-box">
                <pre><code>{clean_prompt}</code></pre>
            </div>
            <button class="btn-copy" onclick="copyPrompt(`{escaped_prompt}`, this)">📋 Sao chép Prompt cho Stitch</button>
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} — Stitch Design Preview</title>
    <style>
        :root {{
            --bg-canvas: {taste['bg_canvas']};
            --bg-surface: {taste['bg_surface']};
            --border-subtle: {taste['border_subtle']};
            --text-primary: {taste['text_primary']};
            --text-secondary: {taste['text_secondary']};
            --brand-primary: {taste['brand_primary']};
            --brand-hover: {taste['brand_primary_hover']};
            --radius-card: 16px;
            --radius-pill: 9999px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 32px 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        header {{ margin-bottom: 40px; text-align: center; }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: var(--radius-pill);
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-weight: 500;
        }}
        h1 {{ font-size: 32px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; }}
        .subtitle {{ color: var(--text-secondary); font-size: 16px; max-width: 600px; margin: 0 auto; }}
        
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            margin: 36px 0 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Swatches Grid */
        .swatches-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 12px;
            margin-bottom: 32px;
        }}
        .swatch {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 10px;
            cursor: pointer;
            transition: transform 0.15s ease;
        }}
        .swatch:hover {{ transform: translateY(-2px); }}
        .color-box {{
            height: 48px;
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.06);
            margin-bottom: 8px;
        }}
        .swatch-name {{ font-size: 12px; font-weight: 600; }}
        .swatch-hex {{ font-size: 11px; color: var(--text-secondary); font-family: monospace; }}

        /* Component Demo */
        .demo-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-card);
            padding: 24px;
            margin-bottom: 32px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
        }}
        .btn-pill {{
            background: var(--brand-primary);
            color: #FFFFFF;
            border: none;
            border-radius: var(--radius-pill);
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .btn-outline {{
            background: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-pill);
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
        }}

        /* Screen Prompts */
        .screen-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-card);
            padding: 20px;
            margin-bottom: 20px;
        }}
        .screen-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }}
        .screen-badge {{
            background: var(--brand-primary);
            color: white;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
        }}
        .screen-title {{ font-size: 18px; font-weight: 600; }}
        .screen-hint {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 12px; }}
        .code-box {{
            background: var(--bg-canvas);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 12px;
            font-family: monospace;
            font-size: 12px;
            color: var(--text-primary);
            overflow-x: auto;
            margin-bottom: 12px;
            white-space: pre-wrap;
        }}
        .btn-copy {{
            background: var(--brand-primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        .btn-copy:hover {{ opacity: 0.9; }}
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #111827;
            color: white;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            display: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge">🎨 Stitch Design Pro Preview</div>
            <h1>{project_name}</h1>
            <p class="subtitle">{taste['name']} — {taste['tagline']}</p>
        </header>

        {custom_card_html}

        <h2 class="section-title">🎨 Bảng màu Design Tokens</h2>
        <div class="swatches-grid">
            <div class="swatch" onclick="copyText('{taste['bg_canvas']}', 'Canvas')">
                <div class="color-box" style="background:{taste['bg_canvas']};"></div>
                <div class="swatch-name">Canvas</div>
                <div class="swatch-hex">{taste['bg_canvas']}</div>
            </div>
            <div class="swatch" onclick="copyText('{taste['bg_surface']}', 'Surface')">
                <div class="color-box" style="background:{taste['bg_surface']};"></div>
                <div class="swatch-name">Surface</div>
                <div class="swatch-hex">{taste['bg_surface']}</div>
            </div>
            <div class="swatch" onclick="copyText('{taste['brand_primary']}', 'Brand Accent')">
                <div class="color-box" style="background:{taste['brand_primary']};"></div>
                <div class="swatch-name">Accent CTA</div>
                <div class="swatch-hex">{taste['brand_primary']}</div>
            </div>
            <div class="swatch" onclick="copyText('{taste['text_primary']}', 'Text Primary')">
                <div class="color-box" style="background:{taste['text_primary']};"></div>
                <div class="swatch-name">Text Primary</div>
                <div class="swatch-hex">{taste['text_primary']}</div>
            </div>
            <div class="swatch" onclick="copyText('{taste['border_subtle']}', 'Border')">
                <div class="color-box" style="background:{taste['border_subtle']};"></div>
                <div class="swatch-name">Hairline Border</div>
                <div class="swatch-hex">{taste['border_subtle']}</div>
            </div>
        </div>

        <h2 class="section-title">🔘 Trải nghiệm Thành phần & Nút bấm</h2>
        <div class="demo-card">
            <button class="btn-pill">Floating Pill Button</button>
            <button class="btn-outline">Outline Action</button>
            <span style="color:var(--text-secondary); font-size:14px;">← Phong cách mềm mại, thanh thoát, không còn vệt thô cứng AI</span>
        </div>

        <h2 class="section-title">📋 Bộ Prompt từng màn hình (Dán vào Stitch)</h2>
        {"".join(screens_cards)}
    </div>

    <div id="toast" class="toast">Đã sao chép!</div>

    <script>
        function copyText(text, label) {{
            navigator.clipboard.writeText(text);
            showToast("Đã chép mã màu " + label + ": " + text);
        }}
        function copyPrompt(text, btn) {{
            navigator.clipboard.writeText(text);
            const oldText = btn.innerText;
            btn.innerText = "✅ Đã sao chép thành công!";
            setTimeout(() => {{ btn.innerText = oldText; }}, 2000);
            showToast("Đã chép prompt vào Clipboard!");
        }}
        function showToast(msg) {{
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.style.display = "block";
            setTimeout(() => {{ t.style.display = "none"; }}, 2500);
        }}
    </script>
</body>
</html>
"""
    return html


# ==============================================================================
# PROJECT LISTING UTILITY
# ==============================================================================
def list_projects():
    """Lists all created projects in the projects/ directory."""
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        print(f"\n{YELLOW}Chưa có dự án nào trong thư mục 'projects/'.{RESET}")
        return

    subdirs = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not subdirs:
        print(f"\n{YELLOW}Chưa có dự án nào trong thư mục 'projects/'.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f" {BOLD}DANH SÁCH DỰ ÁN ĐÃ TẠO ({len(subdirs)} dự án){RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    for idx, d in enumerate(sorted(subdirs), 1):
        p_path = os.path.join(projects_dir, d)
        has_design = "✅ DESIGN.md" if os.path.exists(os.path.join(p_path, "DESIGN.md")) else "❌"
        has_prompts = "✅ STITCH_PROMPTS.md" if os.path.exists(os.path.join(p_path, "STITCH_PROMPTS.md")) else "❌"
        has_preview = "✅ preview.html" if os.path.exists(os.path.join(p_path, "preview.html")) else "❌"
        print(f"  [{idx}] {BOLD}{d}{RESET}")
        print(f"      └─ Đường dẫn: {CYAN}{p_path}/{RESET}")
        print(f"      └─ Tệp: {has_design} | {has_prompts} | {has_preview}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}\n")


# ==============================================================================
# ADAPTIVE DYNAMIC CONSULTATION WIZARD
# ==============================================================================
def interactive_mode():
    """Runs a deeply adaptive, branching design consultation wizard with custom directives."""
    print(f"\n{BOLD}{CYAN}╔═══════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║     🎨  STITCH DESIGN PRO — ADAPTIVE ART DIRECTION CONSULTATION                      ║{RESET}")
    print(f"{BOLD}{CYAN}║     (Khảo sát thích ứng thông minh theo lĩnh vực + Nhập yêu cầu riêng tùy ý)         ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    # 1. Project Info & Core Domain Selection
    print(f"{BOLD}{YELLOW}[Bước 1/6] 📱 THÔNG TIN DỰ ÁN & LĨNH VỰC CỐT LÕI{RESET}")
    project_name = input(f"  ▸ {BOLD}Tên dự án (Project Name){RESET} [My App]: ").strip() or "My App"
    
    print("\n  Chọn lĩnh vực hoạt động của ứng dụng:")
    print("    [1] 📖 Đọc sách, PDF, Tài liệu & Ghi chú (Reader / Books / Docs / Notes)")
    print("    [2] ⚡ Công cụ tính toán, Năng suất & Dev Tools (Calculator / Utility / SaaS / Code)")
    print("    [3] 💳 Tài chính cá nhân, Crypto & Ngân hàng (Fintech / Wallet / Trading)")
    print("    [4] 🧘 Sức khỏe, Thể thao, Thiền định & Thói quen (Health / Fitness / Zen / Habit)")
    print("    [5] 🛍️ Thương mại điện tử, Đặt lịch & Bán lẻ (E-Commerce / Store / Services)")
    print("    [6] ✍️ Lĩnh vực khác (Tự do mô tả)...")
    
    domain_choice = input(f"  ▸ {BOLD}Chọn lĩnh vực [1-6]{RESET} (Mặc định 1): ").strip()
    
    # Adaptive Domain Setup
    domain_key = "reader"
    domain_name = "Đọc sách & Tài liệu"
    query = "Document PDF Reader Tool"
    smart_screens = ["Thư viện tài liệu", "Màn hình đọc sách & ghi chú", "Cài đặt chế độ đọc"]
    
    if domain_choice == "2":
        domain_key = "tool"
        domain_name = "Công cụ tính toán & Dev Tools"
        query = "Productivity Calculator Utility Tool"
        smart_screens = ["Màn tính toán thường", "Tính toán khoa học", "Đổi đơn vị & Lịch sử"]
    elif domain_choice == "3":
        domain_key = "finance"
        domain_name = "Tài chính & Ví điện tử"
        query = "Fintech Wealth Crypto Wallet App"
        smart_screens = ["Tổng quan tài sản & số dư", "Lịch sử giao dịch", "Quản lý ngân sách"]
    elif domain_choice == "4":
        domain_key = "lifestyle"
        domain_name = "Sức khỏe & Thiền định"
        query = "Health Fitness Meditation Tracker"
        smart_screens = ["Bảng thói quen hàng ngày", "Buổi tập luyện / thiền", "Thống kê tiến độ"]
    elif domain_choice == "5":
        domain_key = "commerce"
        domain_name = "Thương mại & Bán lẻ"
        query = "Modern Retail E-Commerce Store"
        smart_screens = ["Khám phá sản phẩm", "Chi tiết sản phẩm & chọn size", "Giỏ hàng & thanh toán"]
    elif domain_choice == "6":
        domain_key = "custom"
        domain_name = input(f"  ▸ {BOLD}Nhập tên lĩnh vực:{RESET} ").strip() or "Custom Digital Product"
        query = input(f"  ▸ {BOLD}Mô tả ngắn gọn về app của bạn:{RESET} ").strip() or "Modern Utility Application"
        smart_screens = ["Màn hình chính / Khám phá", "Màn hình chi tiết nghiệp vụ", "Màn hình cài đặt"]

    # 2. ADAPTIVE PERSONA SELECTION (Filtered & Contextual to Domain)
    print(f"\n{BOLD}{YELLOW}[Bước 2/6] 🎭 GU THẨM MỸ TƯƠNG THÍCH VỚI '{domain_name.upper()}'{RESET}")
    print(f"  {DIM}Các phong cách dưới đây đã được lọc chuẩn xác để ăn khớp với nghiệp vụ của bạn:{RESET}\n")

    if domain_key == "tool":
        print(f"  {BOLD}[1] Linear Obsidian (Sleek Dark Pro) - [KHUYÊN DÙNG CHO CÔNG CỤ]{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Đen sâu huyền bí (OLED), viền kim loại 0.5px, phong cách công cụ đỉnh cao.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Linear, Raycast, Superhuman, Arc Browser\n")
        print(f"  {BOLD}[2] Modern Consumer Fluid (Airbnb / Notion Style){RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Mềm mại, thân thiện, nút bấm bo tròn dễ chạm, không bao giờ thô ráp.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Notion, Airbnb, Spotify\n")
        print(f"  {BOLD}[3] Nordic Zen (Pure Minimalist Keypad){RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Tối giản thanh khiết, không rườm rà, tập trung 100% vào thao tác.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Muji, Nothing OS, Teenage Engineering\n")
        print(f"  {BOLD}[4] Xem tất cả các phong cách khác...{RESET}")
        
        p_choice = input(f"  ▸ {BOLD}Chọn gu thẩm mỹ [1-4]{RESET} (Mặc định [1]): ").strip()
        if p_choice == "2":
            selected_taste_key = "modern_consumer"
        elif p_choice == "3":
            selected_taste_key = "nordic_zen"
        elif p_choice == "4":
            selected_taste_key = "editorial_warmth"
        else:
            selected_taste_key = "linear_obsidian"

    elif domain_key == "reader":
        print(f"  {BOLD}[1] Editorial Warmth (Paper & Craft) - [KHUYÊN DÙNG CHO SÁCH/TÀI LIỆU]{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Nền giấy kem ngà tự nhiên, chữ than chì nhung, ấm áp, chống mỏi mắt.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Apple Books, Craft Docs, Readwise Reader, Kinfolk\n")
        print(f"  {BOLD}[2] Nordic Zen (Clean Minimal Reading){RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Thanh khiết, tĩnh lặng, cực nhiều khoảng thở (whitespace).")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Muji, Nothing OS\n")
        print(f"  {BOLD}[3] Modern Luxury (Editorial Serif){RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Đẳng cấp, font có chân kiêu sa như ấn phẩm thượng lưu.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Vogue, The New York Times\n")
        
        p_choice = input(f"  ▸ {BOLD}Chọn gu thẩm mỹ [1-3]{RESET} (Mặc định [1]): ").strip()
        if p_choice == "2":
            selected_taste_key = "nordic_zen"
        elif p_choice == "3":
            selected_taste_key = "modern_luxury"
        else:
            selected_taste_key = "editorial_warmth"

    elif domain_key == "finance":
        print(f"  {BOLD}[1] Linear Obsidian (Dark Crypto Pro) - [KHUYÊN DÙNG TRADING/FINTECH]{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Đen sâu huyền bí, viền kim loại siêu mảnh, hiện đại, uy quyền.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Linear, Raycast, Vercel\n")
        print(f"  {BOLD}[2] Modern Luxury Wealth{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Đẳng cấp ngân hàng tư nhân, xanh lục bảo, sang trọng.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Bloomberg Markets, Rolex app\n")
        print(f"  {BOLD}[3] Modern Consumer Fluid{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} Trực quan, thân thiện, dễ quản lý chi tiêu như ví điện tử thế hệ mới.")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} Revolut, Notion, Airbnb\n")

        p_choice = input(f"  ▸ {BOLD}Chọn gu thẩm mỹ [1-3]{RESET} (Mặc định [1]): ").strip()
        if p_choice == "2":
            selected_taste_key = "modern_luxury"
        elif p_choice == "3":
            selected_taste_key = "modern_consumer"
        else:
            selected_taste_key = "linear_obsidian"

    else:
        # Generic / Lifestyle / Commerce
        print(f"  {BOLD}[1] Nordic Zen (Pure Minimalism){RESET} — Thanh khiết, tĩnh lặng, ngập tràn khoảng thở.")
        print(f"  {BOLD}[2] Modern Consumer Fluid{RESET} — Mềm mại, trẻ trung, thân thiện như Airbnb/Notion.")
        print(f"  {BOLD}[3] Modern Luxury & Editorial{RESET} — Sang trọng, đẳng cấp thương gia.")
        print(f"  {BOLD}[4] Editorial Warmth{RESET} — Ấm áp, thủ công, nền giấy kem ngà.")
        p_choice = input(f"  ▸ {BOLD}Chọn gu thẩm mỹ [1-4]{RESET} (Mặc định [1]): ").strip()
        if p_choice == "2":
            selected_taste_key = "modern_consumer"
        elif p_choice == "3":
            selected_taste_key = "modern_luxury"
        elif p_choice == "4":
            selected_taste_key = "editorial_warmth"
        else:
            selected_taste_key = "nordic_zen"

    selected_persona = TASTE_PERSONAS[selected_taste_key]
    print(f"  👉 {GREEN}Đã chọn linh hồn:{RESET} {BOLD}{selected_persona['name']}{RESET}")

    # 3. ADAPTIVE DOMAIN-SPECIFIC INTERACTION DILEMMA
    print(f"\n{BOLD}{YELLOW}[Bước 3/6] 📐 TRẢI NGHIỆM TƯƠNG TÁC ĐẶC THÙ CHO '{domain_name.upper()}'{RESET}")
    
    layout_mode = "borderless"
    btn_mode = "pill"
    typography_mode = "tech_sans" if domain_key in ["tool", "finance"] else "editorial_serif"

    if domain_key == "tool":
        print("  Hỏi về trải nghiệm bàn phím & hiển thị dữ liệu (Chống thô cứng):")
        print("    [1] 💊 Phím số bo tròn Capsule/Pill (Chạm cực êm, hiển thị số lớn, không thô) [Khuyên dùng]")
        print("    [2] 🌊 Bàn phím số phẳng tối giản không viền (Borderless Flat Keypad)")
        print("    [3] ⚡ Bố cục kỹ thuật số chuyên nghiệp (Pro Compact Grid)")
        t_choice = input(f"  ▸ {BOLD}Chọn kiểu trải nghiệm [1-3]{RESET} (Mặc định [1]): ").strip()
        if t_choice == "2":
            layout_mode = "borderless"
            btn_mode = "minimal"
        elif t_choice == "3":
            layout_mode = "grouped"
            btn_mode = "soft"
        else:
            layout_mode = "grouped"
            btn_mode = "pill"
        typography_mode = "tech_sans"

    elif domain_key == "reader":
        print("  Hỏi về trải nghiệm đọc sách & chú thích:")
        print("    [1] 🌊 Trang sách không viền (Borderless), thanh công cụ chú thích nổi Floating Pill [Khuyên dùng]")
        print("    [2] 📱 Bố cục Grouped Inset Sheet, thẻ phân trang rõ ràng")
        r_choice = input(f"  ▸ {BOLD}Chọn kiểu trải nghiệm [1-2]{RESET} (Mặc định [1]): ").strip()
        layout_mode = "borderless" if r_choice != "2" else "grouped"
        btn_mode = "pill"
        typography_mode = "editorial_serif"

    elif domain_key == "finance":
        print("  Hỏi về hiển thị số dư & giao dịch:")
        print("    [1] 🌊 Dòng tiền phẳng không viền (Borderless Stream), số tiền lớn phân cấp sắc nét [Khuyên dùng]")
        print("    [2] 📱 Thẻ tài sản Grouped Inset Cards theo từng tài khoản/ví")
        f_choice = input(f"  ▸ {BOLD}Chọn kiểu trải nghiệm [1-2]{RESET} (Mặc định [1]): ").strip()
        layout_mode = "borderless" if f_choice != "2" else "grouped"
        btn_mode = "pill"
        typography_mode = "tech_sans"

    else:
        print("  Hỏi về triết lý bố cục chống 'Bệnh đóng hộp':")
        print("    [1] 🌊 Borderless & Fluid (Khoảng trắng tự nhiên & hairline 0.5px) [Khuyên dùng]")
        print("    [2] 📱 Soft Grouped Inset (Khối bo góc mềm 18-24px kiểu iOS)")
        g_choice = input(f"  ▸ {BOLD}Chọn bố cục [1-2]{RESET} (Mặc định [1]): ").strip()
        layout_mode = "borderless" if g_choice != "2" else "grouped"
        btn_mode = "pill"
        typography_mode = "modern_sans"

    # 4. ADAPTIVE COLOR ATMOSPHERE & CONTRAST HARMONY
    print(f"\n{BOLD}{YELLOW}[Bước 4/6] 🖌️ NHIỆT ĐỘ MÀU SẮC & BẦU KHÔNG KHÍ{RESET}")
    print(f"  [1] 💎 Giữ nguyên Palette tối ưu của {selected_persona['name']}")
    print(f"      └─ Canvas: {selected_persona['bg_canvas']} | Chữ: {selected_persona['text_primary']} | Accent: {selected_persona['brand_primary']}")
    
    if selected_persona['bg_canvas'].startswith("#0") or selected_persona['bg_canvas'].startswith("#1"):
        # Dark theme is active -> Offer light contrast alternative
        print("  [2] ☕ Đổi sang Tông Sáng giấy ngà (Warm Cream #FAF8F5 / Hổ phách #B45309)")
        print("  [3] 🎨 Tự nhập mã Hex màu Accent riêng...")
    else:
        # Light theme is active -> Offer dark contrast alternative
        print("  [2] 🌑 Đổi sang Tông Tối Obsidian (Deep Dark #090A0F / Tím điện #6366F1)")
        print("  [3] 🎨 Tự nhập mã Hex màu Accent riêng...")

    color_choice = input(f"  ▸ {BOLD}Chọn bầu không khí màu [1-3]{RESET} (Mặc định [1]): ").strip()
    color_override = {}
    
    if color_choice == "2":
        if selected_persona['bg_canvas'].startswith("#0") or selected_persona['bg_canvas'].startswith("#1"):
            # Switch to warm light
            color_override = {
                "bg_canvas": "#FAF8F5",
                "bg_surface": "#FFFFFF",
                "border_subtle": "#EFECE6",
                "text_primary": "#1C1917",
                "text_secondary": "#78716C",
                "brand_primary": "#B45309",
                "brand_primary_hover": "#92400E"
            }
        else:
            # Switch to dark obsidian
            color_override = {
                "bg_canvas": "#090A0F",
                "bg_surface": "#12141A",
                "border_subtle": "#1F232D",   # Fixed dark metallic border!
                "text_primary": "#F1F5F9",
                "text_secondary": "#94A3B8",  # Fixed dark muted text!
                "brand_primary": "#6366F1",
                "brand_primary_hover": "#4F46E5"
            }
    elif color_choice == "3":
        custom_accent = input(f"    ▸ {BOLD}Nhập mã Hex màu Accent bạn muốn (ví dụ #059669, #EA580C):{RESET} ").strip()
        if custom_accent.startswith("#") and len(custom_accent) in [4, 7]:
            color_override = {"brand_primary": custom_accent, "brand_primary_hover": custom_accent}

    # Build the harmonized taste profile
    taste = build_taste_profile(
        taste_key=selected_taste_key,
        color_override=color_override,
        button_mode=btn_mode,
        typography_mode=typography_mode
    )

    # 5. ADAPTIVE TARGET SCREENS & DEDICATED PROJECT FOLDER
    project_slug = slugify(project_name)
    default_project_dir = os.path.join("projects", project_slug)

    print(f"\n{BOLD}{YELLOW}[Bước 5/6] 🎯 DANH SÁCH MÀN HÌNH MỤC TIÊU & THƯ MỤC LƯU{RESET}")
    platform = input(f"  ▸ {BOLD}Nền tảng mục tiêu (mobile / web){RESET} [mobile]: ").strip() or "mobile"
    dir_input = input(f"  ▸ {BOLD}Thư mục lưu dự án (tránh ghi đè){RESET} [{default_project_dir}]: ").strip()
    project_dir = dir_input or default_project_dir

    smart_default_str = ", ".join(smart_screens)
    print(f"\n  💡 Gợi ý màn hình chuẩn cho {BOLD}{domain_name}{RESET}:")
    print(f"     {CYAN}{smart_default_str}{RESET}")
    screens_input = input(f"  ▸ {BOLD}Nhập danh sách màn hình (Enter để nhận gợi ý trên):{RESET} ").strip()
    
    if screens_input:
        target_screens = [s.strip() for s in screens_input.split(",") if s.strip()]
    else:
        target_screens = smart_screens

    # 6. FREE-FORM CUSTOM DIRECTIVES & SPECIAL WISHES (Crucial feature!)
    print(f"\n{BOLD}{YELLOW}[Bước 6/6] ✍️ YÊU CẦU ĐẶC BIỆT & RÀNG BUỘC RIÊNG (Custom Directives){RESET}")
    print(f"  {DIM}Bạn có mong muốn hoặc yêu cầu riêng nào để giao diện hoàn toàn theo ý bạn không?{RESET}")
    print(f"  {DIM}Ví dụ: 'Nút AC và nút = có màu cam nổi bật', 'Font số hiển thị dạng Monospace', 'Cấm icon màu mè'...{RESET}")
    custom_directives = input(f"  ▸ {BOLD}Nhập yêu cầu riêng (Nhấn Enter nếu không có):{RESET} ").strip()

    # SUMMARY CARD BEFORE GENERATING
    print(f"\n{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f" {BOLD}TỔNG KẾT BẢN THIẾT KẾ NGHỆ THUẬT (DESIGN DNA SUMMARY){RESET}")
    print(f"{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  • Dự án:            {BOLD}{project_name}{RESET} ({platform.upper()})")
    print(f"  • Lĩnh vực:         {domain_name}")
    print(f"  • Thư mục riêng:    {CYAN}{project_dir}/{RESET}")
    print(f"  • Linh hồn thẩm mỹ: {CYAN}{taste['name']}{RESET}")
    print(f"  • Bố cục:           {GREEN}{layout_mode.upper()} (Chống đóng hộp){RESET}")
    print(f"  • Bảng màu:         Canvas: {taste['bg_canvas']} | Surface: {taste['bg_surface']} | Accent: {taste['brand_primary']}")
    print(f"  • Typography:       {typography_mode.upper()}")
    print(f"  • Phong cách nút:   {btn_mode.upper()} Action")
    print(f"  • Số màn hình:      {len(target_screens)} màn hình ({', '.join(target_screens)})")
    if custom_directives:
        print(f"  • Yêu cầu riêng:    {YELLOW}{custom_directives}{RESET}")
    print(f"{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}\n")

    confirm = input(f"👉 {BOLD}Xác nhận tạo trọn bộ sản phẩm chất lượng cao? [Y/n]:{RESET} ").strip().lower()
    if confirm == "n":
        print("❌ Đã hủy thao tác.")
        return

    os.makedirs(project_dir, exist_ok=True)
    design_md_file = os.path.join(project_dir, "DESIGN.md")
    prompt_suite_file = os.path.join(project_dir, "STITCH_PROMPTS.md")
    preview_html_file = os.path.join(project_dir, "preview.html")
    tokens_css_file = os.path.join(project_dir, "tokens.css")
    tokens_kt_file = os.path.join(project_dir, f"{pascal_case(project_name)}Tokens.kt")

    print(f"\n⚙️  {CYAN}Đang xuất bản trọn bộ sản phẩm vào '{project_dir}/'...{RESET}")

    # 1. Generate DESIGN.md
    content = generate_design_md(
        project_name=project_name,
        query=query,
        taste=taste,
        layout_mode=layout_mode,
        platform=platform,
        target_screens=target_screens,
        custom_directives=custom_directives
    )
    with open(design_md_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {GREEN}1. Design System Specification:{RESET} '{design_md_file}'")

    # 2. Generate STITCH_PROMPTS.md
    prompt_suite_content = generate_stitch_prompt_suite(project_name, target_screens, content, custom_directives)
    with open(prompt_suite_file, "w", encoding="utf-8") as f:
        f.write(prompt_suite_content)
    print(f"  ✅ {GREEN}2. Bộ Prompt đa màn hình (Gọn + Độc lập):{RESET} '{prompt_suite_file}'")

    # 3. Generate preview.html
    preview_html_content = generate_preview_html(project_name, taste, target_screens, custom_directives)
    with open(preview_html_file, "w", encoding="utf-8") as f:
        f.write(preview_html_content)
    print(f"  ✅ {GREEN}3. Dashboard xem trước trực quan (Web):{RESET} '{preview_html_file}'")

    # 4. Generate tokens.css
    tokens_css_content = generate_tokens_css(project_name, taste)
    with open(tokens_css_file, "w", encoding="utf-8") as f:
        f.write(tokens_css_content)
    print(f"  ✅ {GREEN}4. Mã nguồn Tokens CSS (Web/Tailwind):{RESET} '{tokens_css_file}'")

    # 5. Generate ThemeTokens.kt
    tokens_kt_content = generate_tokens_kt(project_name, taste)
    with open(tokens_kt_file, "w", encoding="utf-8") as f:
        f.write(tokens_kt_content)
    print(f"  ✅ {GREEN}5. Mã nguồn Tokens Kotlin (Jetpack Compose):{RESET} '{tokens_kt_file}'")

    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f" {BOLD}🎉 HOÀN TẤT TRỌN BỘ SẢN PHẨM CHO '{project_name.upper()}':{RESET}")
    print(f"  👉 Mở file {BOLD}{preview_html_file}{RESET} trên trình duyệt để kiểm tra màu sắc và copy prompt 1-click!")
    print(f"  👉 Dán {BOLD}{design_md_file}{RESET} lên Google Stitch canvas.")
    print(f"  👉 Mang {BOLD}{tokens_css_file}{RESET} hoặc {BOLD}{tokens_kt_file}{RESET} vào codebase của bạn để triển khai thực tế!")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Stitch Design Pro — Generate High-Aesthetic DESIGN.md for Google Stitch"
    )
    parser.add_argument("query", nargs="?", default="", help="App description or industry")
    parser.add_argument("-p", "--project", default="App Project", help="Project name")
    parser.add_argument("--platform", default="mobile", choices=["mobile", "web"], help="Target platform")
    parser.add_argument("--taste", default="editorial_warmth", choices=list(TASTE_PERSONAS.keys()), help="Aesthetic taste engine")
    parser.add_argument("-o", "--output-dir", default="", help="Custom output directory (default: projects/<project-slug>)")
    parser.add_argument("--prompt-for", help="Also generate an enhanced Stitch prompt for a specific screen")
    parser.add_argument("--custom", default="", help="Custom directives / special wishes")
    parser.add_argument("--list", action="store_true", help="List all generated projects")
    parser.add_argument("--interactive", action="store_true", help="Run interactive consultation wizard")

    args = parser.parse_args()

    if args.list:
        list_projects()
        return

    if args.interactive or not args.query:
        interactive_mode()
        return

    project_slug = slugify(args.project)
    project_dir = args.output_dir or os.path.join("projects", project_slug)
    os.makedirs(project_dir, exist_ok=True)

    taste = build_taste_profile(args.taste)
    target_screens = [args.prompt_for] if args.prompt_for else ["Màn hình chính", "Màn hình chi tiết", "Màn hình cài đặt"]

    design_md_file = os.path.join(project_dir, "DESIGN.md")
    prompt_suite_file = os.path.join(project_dir, "STITCH_PROMPTS.md")
    preview_html_file = os.path.join(project_dir, "preview.html")
    tokens_css_file = os.path.join(project_dir, "tokens.css")
    tokens_kt_file = os.path.join(project_dir, f"{pascal_case(args.project)}Tokens.kt")

    content = generate_design_md(
        project_name=args.project,
        query=args.query,
        taste=taste,
        platform=args.platform,
        target_screens=target_screens,
        custom_directives=args.custom
    )

    with open(design_md_file, "w", encoding="utf-8") as f:
        f.write(content)
    with open(prompt_suite_file, "w", encoding="utf-8") as f:
        f.write(generate_stitch_prompt_suite(args.project, target_screens, content, args.custom))
    with open(preview_html_file, "w", encoding="utf-8") as f:
        f.write(generate_preview_html(args.project, taste, target_screens, args.custom))
    with open(tokens_css_file, "w", encoding="utf-8") as f:
        f.write(generate_tokens_css(args.project, taste))
    with open(tokens_kt_file, "w", encoding="utf-8") as f:
        f.write(generate_tokens_kt(args.project, taste))

    print(f"✨ Successfully generated project bundle in '{project_dir}/':")
    print(f"   • {design_md_file}")
    print(f"   • {prompt_suite_file}")
    print(f"   • {preview_html_file}")
    print(f"   • {tokens_css_file}")
    print(f"   • {tokens_kt_file}")


if __name__ == "__main__":
    main()
