#!/usr/bin/env python3
"""
Generate LinkedIn carousel images from weekly FDE Pulse data.

Creates 6 branded PNG slides (1080x1350) + optional PDF.

Slides:
1. Cover: FDE PULSE + key stats
2. Top Tools (from market_intelligence)
3. Salary by Seniority (from comp_analysis.by_seniority)
4. Top Paying FDE Roles (from comp_analysis.top_paying_roles)
5. Salary by Metro (from comp_analysis.by_metro)
6. CTA: fdepulse.com/newsletter

Usage:
    python scripts/generate_linkedin_carousel.py              # Generate PNGs
    python scripts/generate_linkedin_carousel.py --pdf        # Also combine into PDF
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config — FDE Pulse (amber on dark navy)
# ---------------------------------------------------------------------------

W, H = 1080, 1350

NAVY = (15, 25, 35)            # #0F1923
CARD = (22, 34, 50)            # #162232
ACCENT = (245, 158, 11)        # #F59E0B amber
ACCENT_LIGHT = (251, 191, 36)  # #FBBF24
ACCENT_DIM = (217, 119, 6)     # #D97706
GREEN = (74, 222, 128)         # #4ade80
RED = (248, 113, 113)          # #f87171
WHITE = (255, 255, 255)
GRAY_200 = (226, 232, 240)
GRAY_400 = (148, 163, 184)
GRAY_500 = (100, 116, 139)

BRAND_NAME = "FDE PULSE"
BRAND_TAGLINE = "Forward Deployed Engineer Market Intelligence"
SITE_DOMAIN = "fdepulse.com"
SITE_URL = "fdepulse.com/newsletter"
PDF_FILENAME = "fde-pulse-carousel.pdf"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'carousel')

TOOL_DISPLAY = {
    'Aws': 'AWS', 'Gcp': 'GCP', 'Pytorch': 'PyTorch',
    'Tensorflow': 'TensorFlow', 'Langchain': 'LangChain',
    'Llamaindex': 'LlamaIndex', 'Openai': 'OpenAI',
    'Crewai': 'CrewAI', 'Autogen': 'AutoGen',
    'Hugging Face': 'Hugging Face', 'Prompt Engineering': 'Prompt Eng.',
    'Power Bi': 'Power BI', 'Hubspot': 'HubSpot',
    'Vertex Ai': 'Vertex AI', 'Semantic Kernel': 'Semantic Kernel',
    'Rag': 'RAG', 'Typescript': 'TypeScript', 'Javascript': 'JavaScript',
    'Nodejs': 'Node.js',
}


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def get_font(size, bold=False):
    candidates = []
    if bold:
        candidates = [
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        ]
    else:
        candidates = [
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_rounded_rect(draw, xy, fill, radius=16):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_bar(draw, x, y, width, height, color):
    if width > 0:
        draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill=color)


def slide_header(draw, title, subtitle=None):
    font_title = get_font(42, bold=True)
    draw.text((60, 60), title, fill=WHITE, font=font_title)
    draw.rectangle((60, 120, 200, 124), fill=ACCENT)
    y = 140
    if subtitle:
        font_sub = get_font(24)
        draw.text((60, y), subtitle, fill=GRAY_400, font=font_sub)
        y += 40
    return y + 20


def slide_footer(draw, page_num, total_pages):
    font_footer = get_font(20)
    font_brand = get_font(22, bold=True)
    draw.rectangle((60, H - 100, W - 60, H - 99), fill=GRAY_500)
    draw.text((60, H - 80), BRAND_NAME, fill=ACCENT, font=font_brand)
    page_text = f"{page_num}/{total_pages}"
    bbox = draw.textbbox((0, 0), page_text, font=font_footer)
    draw.text((W - 60 - (bbox[2] - bbox[0]), H - 76), page_text, fill=GRAY_400, font=font_footer)
    draw.text((60, H - 52), SITE_DOMAIN, fill=GRAY_500, font=get_font(16))


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data():
    with open(os.path.join(DATA_DIR, 'market_intelligence.json')) as f:
        mi = json.load(f)
    with open(os.path.join(DATA_DIR, 'comp_analysis.json')) as f:
        ca = json.load(f)
    return mi, ca


# ---------------------------------------------------------------------------
# Slide generators
# ---------------------------------------------------------------------------

def make_cover(mi, ca, date_str, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    font_big = get_font(56, bold=True)
    font_sub = get_font(28)
    font_hook = get_font(26, bold=True)
    font_stat_num = get_font(64, bold=True)
    font_stat_label = get_font(22)

    # Title
    draw.text((60, 120), "FDE", fill=ACCENT, font=font_big)
    draw.text((60, 190), "PULSE", fill=WHITE, font=font_big)
    draw.rectangle((60, 270, 200, 276), fill=ACCENT)
    draw.text((60, 300), f"Week of {date_str}", fill=GRAY_400, font=font_sub)

    # Hook
    total_jobs = mi.get('total_jobs', 0)
    salary_stats = ca.get('salary_stats', {})
    median_k = int(salary_stats.get('median', 0) / 1000)
    hook_lines = [
        f"{total_jobs:,} active Forward Deployed",
        f"Engineer roles. Median ${median_k}K.",
        "Here's where they're hiring.",
    ]
    y_hook = 350
    for line in hook_lines:
        draw.text((60, y_hook), line, fill=WHITE, font=font_hook)
        y_hook += 36

    # Stat cards
    disclosure = ca.get('disclosure_rate', 0)
    by_remote = ca.get('by_remote', {})
    remote_count = by_remote.get('remote', {}).get('count', 0)
    remote_pct = round(remote_count / total_jobs * 100) if total_jobs > 0 else 0

    card_w = (W - 120 - 30) // 3
    y_card = 510

    for i, (val, label) in enumerate([
        (f"{total_jobs:,}", "FDE Roles"),
        (f"${median_k}K", "Median Salary"),
        (f"{remote_pct}%", "Remote-Friendly"),
    ]):
        x = 60 + i * (card_w + 15)
        draw_rounded_rect(draw, (x, y_card, x + card_w, y_card + 180), fill=CARD)
        bbox = draw.textbbox((0, 0), val, font=font_stat_num)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (card_w - text_w) // 2, y_card + 30), val, fill=ACCENT, font=font_stat_num)
        bbox = draw.textbbox((0, 0), label, font=font_stat_label)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (card_w - text_w) // 2, y_card + 120), label, fill=GRAY_400, font=font_stat_label)

    draw.text((60, H - 200), "Swipe for the full breakdown", fill=GRAY_200, font=font_sub)
    draw.text((60, H - 155), "Tools  •  Salary  •  Top Roles  •  Geography",
              fill=GRAY_400, font=font_stat_label)

    slide_footer(draw, 1, total_pages)
    return img


def make_tools_slide(mi, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Top Tools in Demand", "Most-mentioned skills across FDE job posts")

    font_tool = get_font(26, bold=True)
    font_count = get_font(22)

    tools = mi.get('tools', {})
    sorted_tools = sorted(tools.items(), key=lambda x: -x[1])[:8]
    max_count = sorted_tools[0][1] if sorted_tools else 1
    total_jobs = mi.get('total_jobs', 1)

    for i, (name, count) in enumerate(sorted_tools):
        display_name = TOOL_DISPLAY.get(name, name)
        pct = round(count / total_jobs * 100, 1)

        draw_rounded_rect(draw, (60, y, W - 60, y + 110), fill=CARD)

        rank_font = get_font(20, bold=True)
        draw.text((80, y + 12), f"#{i+1}", fill=ACCENT_LIGHT, font=rank_font)
        draw.text((130, y + 10), display_name, fill=WHITE, font=font_tool)

        count_text = f"{count:,} mentions ({pct}%)"
        draw.text((130, y + 48), count_text, fill=GRAY_400, font=font_count)

        bar_w = int(count / max_count * (W - 200))
        draw_bar(draw, 130, y + 82, bar_w, 8, ACCENT)

        y += 125

    slide_footer(draw, 2, total_pages)
    return img


def make_seniority_slide(ca, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Salary by Seniority", "Median base across roles with disclosed pay")

    font_level = get_font(28, bold=True)
    font_salary = get_font(48, bold=True)
    font_count = get_font(22)
    font_range = get_font(20)

    by_seniority = ca.get('by_seniority', {})
    levels_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Director', 'VP']
    rows = []
    for lvl in levels_order:
        if lvl in by_seniority and by_seniority[lvl].get('count', 0) > 0:
            rows.append((lvl, by_seniority[lvl]))
    rows = rows[:5]

    if not rows:
        draw.text((60, y), "Not enough disclosed-salary data this week.",
                  fill=GRAY_200, font=font_level)
    else:
        max_med = max(d.get('median', 0) for _, d in rows) if rows else 1
        for level, data in rows:
            med = data.get('median', 0)
            cnt = data.get('count', 0)
            min_avg = int(data.get('min_base_avg', 0) / 1000)
            max_avg = int(data.get('max_base_avg', 0) / 1000)
            med_k = int(med / 1000)

            draw_rounded_rect(draw, (60, y, W - 60, y + 160), fill=CARD)
            draw.text((80, y + 18), level.upper(), fill=GRAY_400,
                      font=get_font(16, bold=True))
            draw.text((80, y + 50), f"${med_k}K", fill=ACCENT, font=font_salary)
            draw.text((80, y + 110), f"Range ${min_avg}K–${max_avg}K  •  {cnt:,} roles",
                      fill=GRAY_400, font=font_range)

            bar_w = int(med / max_med * (W - 200)) if max_med > 0 else 0
            draw_bar(draw, 80, y + 142, bar_w, 6, ACCENT_DIM)

            y += 175

    slide_footer(draw, 3, total_pages)
    return img


def make_top_roles_slide(ca, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Top Paying FDE Roles", "Highest disclosed base salaries this week")

    font_title = get_font(22, bold=True)
    font_company = get_font(20)
    font_salary = get_font(24, bold=True)

    top_roles = ca.get('top_paying_roles', [])[:6]

    if not top_roles:
        draw.text((60, y), "No disclosed top roles available this week.",
                  fill=GRAY_200, font=font_title)
    else:
        for r in top_roles:
            title = r.get('title', '')
            company = r.get('company', 'Unknown')
            sal_max = r.get('salary_max', 0)
            sal_min = r.get('salary_min', 0)
            sal_max_k = int(sal_max / 1000) if sal_max else 0
            sal_min_k = int(sal_min / 1000) if sal_min else 0

            draw_rounded_rect(draw, (60, y, W - 60, y + 150), fill=CARD)

            # Wrap title to 2 lines if needed (~38 char per line)
            title_words = title.split()
            line1, line2 = '', ''
            for w in title_words:
                if len(line1) + len(w) < 38:
                    line1 = (line1 + ' ' + w).strip()
                elif len(line2) + len(w) < 38:
                    line2 = (line2 + ' ' + w).strip()
                else:
                    line2 = (line2 + '…') if not line2.endswith('…') else line2
                    break
            draw.text((80, y + 18), line1, fill=WHITE, font=font_title)
            if line2:
                draw.text((80, y + 50), line2, fill=WHITE, font=font_title)
                draw.text((80, y + 92), company, fill=GRAY_400, font=font_company)
            else:
                draw.text((80, y + 50), company, fill=GRAY_400, font=font_company)

            sal_text = f"${sal_min_k}–${sal_max_k}K" if sal_min_k else f"${sal_max_k}K"
            bbox = draw.textbbox((0, 0), sal_text, font=font_salary)
            draw.text((W - 80 - (bbox[2] - bbox[0]), y + 20), sal_text,
                      fill=ACCENT, font=font_salary)

            y += 165

    slide_footer(draw, 4, total_pages)
    return img


def make_metros_slide(ca, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Where FDEs Are Hiring", "Median salary by metro (min 5 disclosed roles)")

    font_metro = get_font(26, bold=True)
    font_salary = get_font(28, bold=True)
    font_count = get_font(20)

    by_metro = ca.get('by_metro', {})
    # Filter out Unknown and tiny samples
    rows = [(m, d) for m, d in by_metro.items()
            if m and m.lower() != 'unknown' and d.get('count', 0) >= 5]
    rows.sort(key=lambda x: -x[1].get('median', 0))
    rows = rows[:7]

    if not rows:
        draw.text((60, y), "Not enough metro-level data this week.",
                  fill=GRAY_200, font=font_metro)
    else:
        max_med = rows[0][1].get('median', 1)
        for i, (metro, data) in enumerate(rows):
            med = data.get('median', 0)
            cnt = data.get('count', 0)
            med_k = int(med / 1000)

            draw_rounded_rect(draw, (60, y, W - 60, y + 110), fill=CARD)

            draw.text((80, y + 12), f"#{i+1}  {metro}", fill=WHITE, font=font_metro)
            draw.text((80, y + 50), f"{cnt:,} roles", fill=GRAY_400, font=font_count)

            sal_text = f"${med_k}K"
            bbox = draw.textbbox((0, 0), sal_text, font=font_salary)
            draw.text((W - 80 - (bbox[2] - bbox[0]), y + 30), sal_text,
                      fill=ACCENT, font=font_salary)

            bar_w = int(med / max_med * (W - 200))
            draw_bar(draw, 80, y + 82, bar_w, 6, ACCENT_DIM)

            y += 125

    slide_footer(draw, 5, total_pages)
    return img


def make_cta_slide(mi, ca, total_pages):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    font_big = get_font(48, bold=True)
    font_med = get_font(28)
    font_url = get_font(28, bold=True)
    font_bullet = get_font(24)

    y = 200
    draw.text((60, y), "Tracking the FDE", fill=WHITE, font=font_big)
    y += 70
    draw.text((60, y), "job market", fill=ACCENT, font=font_big)
    y += 70
    draw.text((60, y), "every week.", fill=ACCENT, font=font_big)

    y += 100
    draw.rectangle((60, y, 200, y + 4), fill=ACCENT)
    y += 30

    total_jobs = mi.get('total_jobs', 0)
    median_k = int(ca.get('salary_stats', {}).get('median', 0) / 1000)
    disclosure = ca.get('disclosure_rate', 0)

    bullets = [
        f"{total_jobs:,} FDE roles tracked weekly",
        f"Median base: ${median_k}K",
        f"{disclosure}% of roles disclose salary",
        "Free weekly email, every Monday",
    ]
    for bullet in bullets:
        draw.text((80, y), f"•  {bullet}", fill=GRAY_200, font=font_bullet)
        y += 42

    y += 40
    draw_rounded_rect(draw, (60, y, W - 60, y + 80), fill=ACCENT)
    bbox = draw.textbbox((0, 0), SITE_URL, font=font_url)
    text_w = bbox[2] - bbox[0]
    draw.text(((W - text_w) // 2, y + 25), SITE_URL, fill=NAVY, font=font_url)

    y += 120
    draw.text((60, y), "Follow for weekly FDE market data", fill=GRAY_400, font=font_med)

    slide_footer(draw, total_pages, total_pages)
    return img


# ---------------------------------------------------------------------------
# LinkedIn post text
# ---------------------------------------------------------------------------

def generate_post_text(mi, ca, date_str):
    total_jobs = mi.get('total_jobs', 0)
    salary_stats = ca.get('salary_stats', {})
    median_k = int(salary_stats.get('median', 0) / 1000)
    disclosure = ca.get('disclosure_rate', 0)
    tools = mi.get('tools', {})
    top_tool = sorted(tools.items(), key=lambda x: -x[1])[0] if tools else None

    hook = f"{total_jobs:,} active Forward Deployed Engineer roles tracked this week. Median base ${median_k}K."

    tool_line = ""
    if top_tool:
        tool_name = TOOL_DISPLAY.get(top_tool[0], top_tool[0])
        tool_pct = round(top_tool[1] / total_jobs * 100) if total_jobs else 0
        tool_line = f"\n→ {tool_name} appears in {tool_pct}% of postings"

    post = f"""{hook}

This week's FDE Pulse:

→ {total_jobs:,} FDE roles tracked
→ ${median_k}K median base salary
→ {disclosure}% of roles disclose pay{tool_line}

Swipe for the full breakdown ↓

#ForwardDeployedEngineer #FDE #AIJobs #Salary #JobMarket
"""

    path = os.path.join(OUTPUT_DIR, 'post.txt')
    with open(path, 'w') as f:
        f.write(post)
    print(f"  Post: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Generate LinkedIn carousel images')
    parser.add_argument('--pdf', action='store_true', help='Also combine slides into a PDF')
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mi, ca = load_data()
    date_str = datetime.now().strftime('%B %d, %Y')

    total_pages = 6
    slides = [
        make_cover(mi, ca, date_str, total_pages),
        make_tools_slide(mi, total_pages),
        make_seniority_slide(ca, total_pages),
        make_top_roles_slide(ca, total_pages),
        make_metros_slide(ca, total_pages),
        make_cta_slide(mi, ca, total_pages),
    ]

    for i, slide in enumerate(slides, 1):
        path = os.path.join(OUTPUT_DIR, f'slide-{i:02d}.png')
        slide.save(path, 'PNG', quality=95)
        print(f"  Saved: {path}")

    if args.pdf:
        pdf_path = os.path.join(OUTPUT_DIR, PDF_FILENAME)
        rgb_slides = [s.convert('RGB') for s in slides]
        rgb_slides[0].save(pdf_path, 'PDF', save_all=True,
                           append_images=rgb_slides[1:], resolution=150)
        print(f"  PDF: {pdf_path}")

    generate_post_text(mi, ca, date_str)

    print(f"\n{len(slides)} carousel slides generated in {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
