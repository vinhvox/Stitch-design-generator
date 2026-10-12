#!/usr/bin/env python3
"""
Stitch Design Pro — Advanced Taste & Aesthetics Consultation Engine
===================================================================
Generates production-grade, aesthetically sophisticated DESIGN.md files,
visual preview.html dashboards, code design tokens (CSS & Kotlin),
and tailored multi-screen prompt suites for Google Stitch (stitch.withgoogle.com).

Explicitly engineered to eliminate:
- "AI Boxy Syndrome" (putting everything in rectangular bordered boxes)
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
    target_screens: Optional[List[str]] = None
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
{screens_section}
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


def generate_stitch_prompt_suite(project_name: str, target_screens: List[str], design_md_content: str) -> str:
    """Generates concise 1-click prompts + standalone full prompts."""
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
- Ergonomics: Use floating pill capsule buttons for primary interactions.
```

#### 📦 Option B: Prompt Độc Lập (Dùng khi mở phiên chat mới trong Stitch)
```text
You are a World-Class Principal Product Designer & Art Director building "{project_name}".
Generate Screen #{idx+1}: "{screen.strip()}".

CRITICAL DIRECTIVES:
1. ANTI-BOXY: No rectangular card boxes inside card boxes. Use borderless fluid typography.
2. FLOATING ERGONOMICS: Floating pill capsule buttons only. Never stretch heavy black buttons across screen.
3. SPECIFICATION: {ux_hint}

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
    target_screens: List[str]
) -> str:
    """Generates a standalone, beautiful HTML dashboard to preview design tokens and copy prompts."""
    screens_cards = []
    for idx, screen in enumerate(target_screens):
        hint = get_screen_ux_guidance(screen)
        clean_prompt = f"""You are a Principal Product Designer building "{project_name}".
Create Screen #{idx+1}: "{screen.strip()}".

STRICT DESIGN SYSTEM INSTRUCTIONS:
- Strictly follow all tokens and rules in the project's DESIGN.md.
- Focus: {hint}
- Anti-Boxy Directive: DO NOT use boxed rectangle cards with 1px borders. Use generous whitespace, borderless typography flow, and hairline dividers.
- Ergonomics: Use floating pill capsule buttons for primary interactions."""

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
# DEEP INTERACTIVE CONSULTATION WIZARD (UPGRADED)
# ==============================================================================
def interactive_mode():
    """Runs a deep, multi-dimensional design consultation wizard with rich formatting."""
    print(f"\n{BOLD}{CYAN}╔═══════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║     🎨  STITCH DESIGN PRO — INTERACTIVE ART DIRECTION CONSULTATION                  ║{RESET}")
    print(f"{BOLD}{CYAN}║     (Tạo DESIGN.md có gu, thanh thoát, xóa sạch hoàn toàn vết tích 'AI-slop')        ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    # 1. Project Info & Category Shortcut
    print(f"{BOLD}{YELLOW}[Bước 1/7] 📱 THÔNG TIN SẢN PHẨM & LĨNH VỰC HOẠT ĐỘNG{RESET}")
    project_name = input(f"  ▸ {BOLD}Tên dự án (Project Name){RESET} [My App]: ").strip() or "My App"
    
    print("\n  Chọn nhanh lĩnh vực sản phẩm của bạn:")
    print("    [1] 📖 Đọc sách, Tài liệu & Ghi chú (PDF Reader / Books / Docs / Notes)")
    print("    [2] 💳 Tài chính, Ví điện tử & Quản lý chi tiêu (Fintech / Crypto / Wallet)")
    print("    [3] ⚡ Công cụ năng suất & Lập trình (Productivity / SaaS / Dev Tools)")
    print("    [4] 🧘 Sức khỏe, Thể thao & Thiền định (Health / Fitness / Zen / Habit)")
    print("    [5] 🛍️ Thương mại điện tử & Thời trang (E-Commerce / Retail / Store)")
    print("    [6] ✍️ Tự nhập mô tả tự do...")
    
    domain_choice = input(f"  ▸ {BOLD}Chọn lĩnh vực [1-6]{RESET} (Mặc định 1): ").strip()
    preset_taste = "editorial_warmth"
    if domain_choice == "2":
        query = f"Fintech Crypto Wealth Management App"
        preset_taste = "linear_obsidian"
    elif domain_choice == "3":
        query = f"Productivity SaaS Tool"
        preset_taste = "linear_obsidian"
    elif domain_choice == "4":
        query = f"Health Fitness Zen Tracker"
        preset_taste = "nordic_zen"
    elif domain_choice == "5":
        query = f"Modern Luxury E-Commerce Fashion Store"
        preset_taste = "modern_luxury"
    elif domain_choice == "6":
        query = input(f"  ▸ {BOLD}Nhập mô tả cụ thể về app của bạn:{RESET} ").strip() or "Tool Application"
    else:
        query = f"Document & PDF Reader Tool with smart annotations"
        preset_taste = "editorial_warmth"

    # 2. Aesthetic Taste Engine (Gu thẩm mỹ)
    print(f"\n{BOLD}{YELLOW}[Bước 2/7] 🎭 GU THẨM MỸ & LINH HỒN HÌNH ẢNH (Aesthetic Persona){RESET}")
    print(f"  {DIM}Định hình toàn bộ cảm xúc, ánh sáng và trải nghiệm của ứng dụng:{RESET}\n")
    
    personas_keys = list(TASTE_PERSONAS.keys())
    for idx, key in enumerate(personas_keys, 1):
        item = TASTE_PERSONAS[key]
        print(f"  {BOLD}[{idx}] {item['name']}{RESET}")
        print(f"      {CYAN}▸ Cảm xúc:{RESET} {item['tagline']}")
        print(f"      {DIM}▸ Đặc trưng:{RESET} {item['description']}")
        print(f"      {GREEN}▸ Hình mẫu:{RESET} {item['analogues']}")
        print(f"      {YELLOW}▸ Phù hợp nhất:{RESET} {item['best_for']}\n")

    default_idx = personas_keys.index(preset_taste) + 1 if preset_taste in personas_keys else 1
    choice_taste = input(f"  ▸ {BOLD}Chọn phong cách [1-{len(personas_keys)}]{RESET} (Mặc định [{default_idx}]): ").strip()
    try:
        taste_idx = int(choice_taste) - 1
        if 0 <= taste_idx < len(personas_keys):
            selected_taste_key = personas_keys[taste_idx]
        else:
            selected_taste_key = preset_taste
    except ValueError:
        selected_taste_key = preset_taste

    selected_persona = TASTE_PERSONAS[selected_taste_key]
    print(f"  👉 {GREEN}Đã chọn linh hồn:{RESET} {BOLD}{selected_persona['name']}{RESET}")

    # 3. Layout Philosophy (Bố cục chống đóng hộp)
    print(f"\n{BOLD}{YELLOW}[Bước 3/7] 📐 TRIẾT LÝ BỐ CỤC (Chống triệt để 'Bệnh đóng hộp' AI){RESET}")
    print("  [1] 🌊 Borderless & Fluid (Khuyên dùng mạnh mẽ):")
    print("      └─ Xóa sạch các thẻ card viền xám. Nội dung nằm trên nền canvas, phân tách bằng")
    print("         khoảng trắng (16-24px) và hairline 0.5px. Xóa sổ cảm giác bảng tính/Excel thô cứng!")
    print("  [2] 📱 Soft Grouped Inset (Chuẩn mực Apple iOS Human Interface):")
    print("      └─ Các khối thông tin bo góc lớn mềm mại (18px-24px), thụt lề 16px, phong cách iOS Settings.")
    print("  [3] 🎈 Floating Canvas (Khung mở & Dock nổi):")
    print("      └─ Nền phẳng hoàn toàn, thanh công cụ điều khiển co lại thành Floating Capsule lơ lửng phía dưới.")
    
    choice_layout = input(f"  ▸ {BOLD}Chọn triết lý bố cục [1-3]{RESET} (Mặc định [1]): ").strip()
    layout_mode = "borderless" if choice_layout != "2" and choice_layout != "3" else ("grouped" if choice_layout == "2" else "floating")

    # 4. Color Atmosphere (Bầu không khí màu sắc)
    print(f"\n{BOLD}{YELLOW}[Bước 4/7] 🖌️ NHIỆT ĐỘ MÀU SẮC & BẦU KHÔNG KHÍ (Color Atmosphere){RESET}")
    print(f"  [1] 💎 Giữ nguyên Palette chuẩn của {selected_persona['name']}")
    print(f"      └─ Canvas: {selected_persona['bg_canvas']} | Chữ: {selected_persona['text_primary']} | Accent: {selected_persona['brand_primary']}")
    print("  [2] ☕ Tông Giấy ngà ấm áp (Warm Cream #FAF8F5 & Hổ phách #B45309):")
    print("      └─ Chống mỏi mắt tuyệt đối khi đọc lâu, cảm giác thủ công tự nhiên như sách giấy.")
    print("  [3] 🌑 Tông Obsidian Tối (Deep Dark #090A0F & Tím điện #6366F1):")
    print("      └─ Đen tuyền sâu thẳm, huyền bí, viền kim loại mảnh 0.5px, siêu tiết kiệm pin OLED.")
    print("  [4] ❄️ Tông Trắng khoáng sản (Pure White #FFFFFF & Xám tro #E5E5E7):")
    print("      └─ Tinh khôi, thanh sạch, phong cách tối giản Bắc Âu / Muji.")
    print("  [5] 🎨 Tự nhập mã màu Accent nhận diện thương hiệu riêng (Custom Hex Code)...")

    choice_color = input(f"  ▸ {BOLD}Chọn bầu không khí màu [1-5]{RESET} (Mặc định [1]): ").strip()
    color_override = {}
    if choice_color == "2":
        color_override = {
            "bg_canvas": "#FAF8F5",
            "bg_surface": "#FFFFFF",
            "border_subtle": "#EFECE6",
            "text_primary": "#1C1917",
            "text_secondary": "#78716C",
            "brand_primary": "#B45309",
            "brand_primary_hover": "#92400E"
        }
    elif choice_color == "3":
        color_override = {
            "bg_canvas": "#090A0F",
            "bg_surface": "#12141A",
            "border_subtle": "#1F232D",   # Corrected dark metallic border
            "text_primary": "#F1F5F9",
            "text_secondary": "#94A3B8",  # Corrected dark muted text
            "brand_primary": "#6366F1",
            "brand_primary_hover": "#4F46E5"
        }
    elif choice_color == "4":
        color_override = {
            "bg_canvas": "#FFFFFF",
            "bg_surface": "#F6F6F7",
            "border_subtle": "#E5E5E7",
            "text_primary": "#111111",
            "text_secondary": "#6E6E73",
            "brand_primary": "#2D3139",
            "brand_primary_hover": "#1A1C20"
        }
    elif choice_color == "5":
        custom_accent = input(f"    ▸ {BOLD}Nhập mã Hex màu Accent bạn muốn (ví dụ #059669, #EA580C):{RESET} ").strip()
        if custom_accent.startswith("#") and len(custom_accent) in [4, 7]:
            color_override = {"brand_primary": custom_accent, "brand_primary_hover": custom_accent}

    # 5. Typography Pairing
    print(f"\n{BOLD}{YELLOW}[Bước 5/7] 🔤 PHONG CÁCH TYPOGRAPHY & CHỮ VIẾT{RESET}")
    print("  [1] 📚 Editorial Serif + Sans (Tiêu đề: Newsreader / Playfair; Nội dung: Inter):")
    print("      └─ Sang trọng, có chiều sâu nghệ thuật, xuất sắc cho app đọc sách, tạp chí, ghi chú.")
    print("  [2] 🔠 Clean Modern Sans (Toàn bộ dùng Inter / SF Pro):")
    print("      └─ Trung tính, thanh sạch, độ dễ đọc (legibility) cao nhất trên mọi màn hình.")
    print("  [3] ⚡ Geometric Tech Sans (Plus Jakarta Sans / Geist):")
    print("      └─ Hiện đại, trẻ trung, sắc sảo cho công cụ SaaS & Dev Tools.")
    
    choice_typo = input(f"  ▸ {BOLD}Chọn Typography [1-3]{RESET} (Mặc định [1]): ").strip()
    typography_mode = "editorial_serif" if choice_typo != "2" and choice_typo != "3" else ("modern_sans" if choice_typo == "2" else "tech_sans")

    # 6. Button & Micro-Interactions (Phong cách nút bấm)
    print(f"\n{BOLD}{YELLOW}[Bước 6/7] 🔘 PHONG CÁCH NÚT BẤM (CTA) & VI TƯƠNG TÁC{RESET}")
    print("  [1] 💊 Floating Pill / Capsule (Nút viên nhộng bo tròn 9999px mềm mại, không bao giờ thô ráp):")
    print("      └─ Khuyên dùng để xóa bỏ vệt thô cứng của AI. Đặt nổi thanh thoát, không che khuất nội dung.")
    print("  [2] 🏷️  Soft Rounded (Bo góc mềm 12px vừa phải, kích thước gọn gàng):")
    print("      └─ Phong cách hiện đại, đĩnh đạc, phù hợp với dashboard hoặc ứng dụng công việc.")
    print("  [3] ✍️  Minimal Text Action (Tối giản hoàn toàn, ưu tiên text link & icon):")
    print("      └─ Tinh khiết tuyệt đối, không dùng khối màu nặng nề.")
    
    choice_btn = input(f"  ▸ {BOLD}Chọn phong cách nút [1-3]{RESET} (Mặc định [1]): ").strip()
    btn_mode = "pill" if choice_btn != "2" and choice_btn != "3" else ("soft" if choice_btn == "2" else "minimal")

    # Build the harmonized taste profile
    taste = build_taste_profile(
        taste_key=selected_taste_key,
        color_override=color_override,
        button_mode=btn_mode,
        typography_mode=typography_mode
    )

    # 7. Target Screens & Output Directory
    project_slug = slugify(project_name)
    default_project_dir = os.path.join("projects", project_slug)

    print(f"\n{BOLD}{YELLOW}[Bước 7/7] 🎯 DANH SÁCH MÀN HÌNH MỤC TIÊU & XUẤT BẢN{RESET}")
    platform = input(f"  ▸ {BOLD}Nền tảng mục tiêu (mobile / web){RESET} [mobile]: ").strip() or "mobile"
    
    dir_input = input(f"  ▸ {BOLD}Thư mục lưu dự án riêng biệt{RESET} [{default_project_dir}]: ").strip()
    project_dir = dir_input or default_project_dir
    
    print("\n  💡 Nhập các màn hình bạn muốn sinh trên Stitch (cách nhau bởi dấu phẩy):")
    print("     Ví dụ: Thư viện tài liệu, Màn hình đọc sách & ghi chú, Cài đặt chế độ đọc")
    screens_input = input(f"  ▸ {BOLD}Danh sách màn hình:{RESET} ").strip()
    
    target_screens = []
    if screens_input:
        target_screens = [s.strip() for s in screens_input.split(",") if s.strip()]
    else:
        target_screens = ["Màn hình chính / Khám phá", "Màn hình chi tiết nghiệp vụ", "Màn hình cài đặt"]

    # SUMMARY CARD BEFORE GENERATING
    print(f"\n{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f" {BOLD}TỔNG KẾT BẢN THIẾT KẾ NGHỆ THUẬT (DESIGN DNA SUMMARY){RESET}")
    print(f"{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  • Dự án:            {BOLD}{project_name}{RESET} ({platform.upper()})")
    print(f"  • Thư mục riêng:    {CYAN}{project_dir}/{RESET}")
    print(f"  • Linh hồn thẩm mỹ: {CYAN}{taste['name']}{RESET}")
    print(f"  • Bố cục:           {GREEN}{layout_mode.upper()} (Chống đóng hộp){RESET}")
    print(f"  • Bảng màu:         Canvas: {taste['bg_canvas']} | Surface: {taste['bg_surface']} | Accent: {taste['brand_primary']}")
    print(f"  • Typography:       {typography_mode.upper()}")
    print(f"  • Phong cách nút:   {btn_mode.upper()} Action")
    print(f"  • Số màn hình:      {len(target_screens)} màn hình ({', '.join(target_screens)})")
    print(f"{BOLD}{GREEN}═══════════════════════════════════════════════════════════════════════════════════════{RESET}\n")

    confirm = input(f"👉 {BOLD}Xác nhận tạo toàn bộ Design System, Code Tokens & Preview? [Y/n]:{RESET} ").strip().lower()
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
        target_screens=target_screens
    )
    with open(design_md_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {GREEN}1. Design System Specification:{RESET} '{design_md_file}'")

    # 2. Generate STITCH_PROMPTS.md
    prompt_suite_content = generate_stitch_prompt_suite(project_name, target_screens, content)
    with open(prompt_suite_file, "w", encoding="utf-8") as f:
        f.write(prompt_suite_content)
    print(f"  ✅ {GREEN}2. Bộ Prompt đa màn hình (Gọn + Độc lập):{RESET} '{prompt_suite_file}'")

    # 3. Generate preview.html
    preview_html_content = generate_preview_html(project_name, taste, target_screens)
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
        target_screens=target_screens
    )

    with open(design_md_file, "w", encoding="utf-8") as f:
        f.write(content)
    with open(prompt_suite_file, "w", encoding="utf-8") as f:
        f.write(generate_stitch_prompt_suite(args.project, target_screens, content))
    with open(preview_html_file, "w", encoding="utf-8") as f:
        f.write(generate_preview_html(args.project, taste, target_screens))
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
