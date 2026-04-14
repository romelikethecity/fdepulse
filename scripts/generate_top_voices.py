#!/usr/bin/env python3
"""Generate Top 25 FDE Voices page. Data in data/top_voices.json."""

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import SITE_NAME, BASE_URL
from templates import get_full_page, get_signup_js

SITE_DIR = 'site'

def load_voices():
    with open('data/top_voices.json', 'r') as f:
        return json.load(f)

def voice_card_html(v):
    tags = ''.join(f'<span class="voice-tag">{t}</span>' for t in v.get("tags", []))
    rank_class = "voice-rank-top" if v["rank"] <= 3 else "voice-rank"
    return f'''<div class="voice-card" id="voice-{v["rank"]}">
    <div class="voice-card-header">
        <div class="{rank_class}">#{v["rank"]}</div>
        <div class="voice-card-info">
            <h3 class="voice-name"><a href="{v["linkedin_url"]}" target="_blank" rel="noopener">{v["name"]}</a></h3>
            <p class="voice-title">{v["title"]} at {v["company"]}</p>
            <div class="voice-tags">{tags}</div>
        </div>
        <a href="{v["linkedin_url"]}" target="_blank" rel="noopener" class="voice-linkedin-btn" aria-label="View {v["name"]} on LinkedIn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
        </a>
    </div>
    <p class="voice-bio">{v["bio"]}</p>
</div>'''

CSS_VOICES = """
.voices-hero { text-align: center; padding: 6rem var(--space-lg) 2rem; max-width: 800px; margin: 0 auto; }
.voices-hero .eyebrow { color: var(--amber); font-family: var(--font-mono); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; }
.voices-hero h1 { font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 700; letter-spacing: -0.5px; margin-bottom: 0.75rem; color: var(--text-primary); }
.voices-subtitle { font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
.voices-meta { font-size: 0.85rem; color: var(--text-muted); }
.voices-content { max-width: 800px; margin: 0 auto; padding: 0 var(--space-lg) var(--space-3xl); }
.voice-methodology { margin-bottom: var(--space-xl); border: 1px solid var(--border); border-radius: var(--radius-lg); background: var(--bg-card); }
.voice-methodology summary { padding: var(--space-md) var(--space-lg); cursor: pointer; font-size: 0.95rem; color: var(--text-primary); font-weight: 600; }
.voice-methodology summary:hover { color: var(--amber); }
.methodology-content { padding: 0 var(--space-lg) var(--space-lg); font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; }
.methodology-content ul { padding-left: var(--space-lg); margin: 0.75rem 0; }
.methodology-content li { margin-bottom: 0.5rem; }
.voices-jump-nav { display: flex; flex-wrap: wrap; gap: 0.25rem; margin-bottom: var(--space-xl); padding: 0.75rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); }
.voice-jump-link { font-size: 0.75rem; font-family: var(--font-mono); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm); color: var(--text-muted); text-decoration: none; transition: background 0.15s, color 0.15s; }
.voice-jump-link:hover { background: var(--amber); color: #0F1923; }
.voices-section-heading { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--amber); color: var(--text-primary); }
.voices-grid { display: flex; flex-direction: column; gap: var(--space-md); margin-bottom: var(--space-2xl); }
.voice-card { border: 1px solid var(--border); border-radius: var(--radius-lg); background: var(--bg-card); padding: var(--space-lg); transition: border-color 0.25s, box-shadow 0.25s; }
.voice-card:hover { border-color: var(--amber); box-shadow: 0 0 20px var(--amber-glow); }
.voice-card-header { display: flex; align-items: flex-start; gap: 0.75rem; }
.voice-rank, .voice-rank-top { font-family: var(--font-mono); font-weight: 700; font-size: 1.1rem; min-width: 2.5rem; text-align: center; flex-shrink: 0; padding-top: 0.15rem; color: var(--text-muted); }
.voice-rank-top { color: var(--amber-light); font-size: 1.25rem; }
.voice-card-info { flex: 1; min-width: 0; }
.voice-name { font-size: 1.1rem; font-weight: 600; margin: 0 0 0.25rem; line-height: 1.3; }
.voice-name a { color: var(--text-primary); text-decoration: none; }
.voice-name a:hover { color: var(--amber-light); }
.voice-title { font-size: 0.85rem; color: var(--text-secondary); margin: 0 0 0.5rem; }
.voice-tags { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.voice-tag { font-size: 0.7rem; font-family: var(--font-mono); padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: var(--amber-ghost); color: var(--amber); font-weight: 500; }
.voice-linkedin-btn { flex-shrink: 0; display: flex; align-items: center; justify-content: center; width: 2.25rem; height: 2.25rem; border-radius: var(--radius-sm); color: var(--text-muted); text-decoration: none; transition: color 0.15s, background 0.15s; }
.voice-linkedin-btn:hover { color: #0077B5; background: rgba(0, 119, 181, 0.15); }
.voice-bio { margin: 0.75rem 0 0; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; padding-left: calc(2.5rem + 0.75rem); }
.voices-share-cta { text-align: center; padding: var(--space-xl) var(--space-lg); max-width: 600px; margin: 0 auto; }
.voices-share-cta h2 { font-size: 1.3rem; margin-bottom: 0.5rem; color: var(--text-primary); }
.voices-share-cta p { color: var(--text-secondary); margin-bottom: 0.5rem; }
@media (max-width: 640px) { .voice-bio { padding-left: 0; } .voice-card-header { flex-wrap: wrap; } .voice-card { position: relative; } .voice-linkedin-btn { position: absolute; top: var(--space-md); right: var(--space-md); } .voices-jump-nav { display: none; } }
"""

def generate_voices_page():
    data = load_voices()
    voices = data["voices"]
    leaders = [v for v in voices if v.get("tier") == "leader"]
    rising = [v for v in voices if v.get("tier") == "rising"]
    last_updated = data.get("last_updated", "2026-04-14")

    jump_links = ''.join(f'<a href="#voice-{v["rank"]}" class="voice-jump-link">#{v["rank"]} {v["name"].split()[0]}</a>' for v in voices)
    leaders_html = ''.join(voice_card_html(v) for v in leaders)
    rising_html = ''.join(voice_card_html(v) for v in rising)

    methodology = f'''<details class="voice-methodology">
    <summary>How We Ranked These Voices</summary>
    <div class="methodology-content">
        <p>{data.get("methodology", "")}</p>
        <ul>
            <li><strong>FDE relevance</strong> (required): Must contribute to the FDE/customer-embedded engineering profession.</li>
            <li><strong>Published work</strong> (30%): Books, newsletters, blog posts, talks that advance the discipline.</li>
            <li><strong>Industry impact</strong> (25%): Building FDE teams, investing in FDE companies, defining the role.</li>
            <li><strong>Content reach</strong> (25%): Newsletter subscribers, LinkedIn following, conference appearances.</li>
            <li><strong>Originality</strong> (20%): Original thinking about customer-embedded engineering.</li>
        </ul>
    </div>
</details>'''

    list_items = ','.join(f'{{"@type":"ListItem","position":{v["rank"]},"item":{{"@type":"Person","name":"{v["name"]}","jobTitle":"{v["title"]}","url":"{v["linkedin_url"]}"}}}}' for v in voices)
    schemas = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ItemList","name":"{data["title"]}","numberOfItems":{len(voices)},"itemListElement":[{list_items}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{data["title"]}","author":{{"@type":"Person","name":"Rome Thorndike"}},"publisher":{{"@type":"Organization","name":"{SITE_NAME}"}},"datePublished":"2026-04-14","dateModified":"{last_updated}","url":"{BASE_URL}/voices/"}}</script>'''

    body = f'''
    <section class="voices-hero">
        <div class="eyebrow">2026 RANKINGS</div>
        <h1>{data["title"]}</h1>
        <p class="voices-subtitle">{data.get("subtitle", "")}</p>
        <p class="voices-meta">Last updated: {last_updated} &middot; {len(voices)} voices ranked</p>
    </section>
    <div class="voices-content">
        {methodology}
        <div class="voices-jump-nav">{jump_links}</div>
        <h2 class="voices-section-heading">Top 10 Leaders</h2>
        <p style="color: var(--text-secondary); margin-bottom: var(--space-md);">The most recognized voices shaping Forward Deployed Engineering.</p>
        <div class="voices-grid">{leaders_html}</div>
        <h2 class="voices-section-heading">Rising Voices (11-25)</h2>
        <p style="color: var(--text-secondary); margin-bottom: var(--space-md);">Engineers, investors, and educators gaining momentum in the FDE community.</p>
        <div class="voices-grid">{rising_html}</div>
    </div>
    <section class="voices-share-cta">
        <h2>Made the List?</h2>
        <p>Share it. Tag us on LinkedIn. We will amplify your post.</p>
        <p>Know someone who should be on next year's list? <a href="mailto:rome@getprovyx.com">Let us know</a>.</p>
    </section>'''

    extra = f"<style>{CSS_VOICES}</style>\n{schemas}"
    html = get_full_page(title="Top 25 FDE Voices of 2026", description="Rankings of the 25 most influential Forward Deployed Engineers, customer engineers, and field engineers shaping the profession.", body_content=body, canonical_path="/voices/", extra_head=extra)
    html = html.replace("</body>", f"{get_signup_js()}\n</body>")

    os.makedirs(os.path.join(SITE_DIR, 'voices'), exist_ok=True)
    with open(os.path.join(SITE_DIR, 'voices', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: /voices/ ({len(voices)} voices)")

if __name__ == '__main__':
    print("Generating Top Voices page...")
    generate_voices_page()
    print("Done!")
