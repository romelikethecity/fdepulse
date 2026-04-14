#!/bin/bash
# Build script for FDE Pulse site
set -uo pipefail

cd "$(dirname "$0")"

echo "=== Building FDE Pulse ==="

# Create directories
mkdir -p site/jobs site/salaries site/companies site/insights site/about site/assets/images site/assets/css

# Brand assets
echo "  Copying brand assets..."
cp brand/favicons/favicon.ico brand/favicons/favicon-16x16.png brand/favicons/favicon-32x32.png \
   brand/favicons/apple-touch-icon.png brand/favicons/android-chrome-192x192.png \
   brand/favicons/android-chrome-512x512.png brand/favicons/mstile-150x150.png site/
cp brand/site.webmanifest site/
cp brand/browserconfig.xml site/
cp brand/svg/logo-mark.svg brand/svg/logo-lockup-horizontal-dark.svg site/assets/images/

# Static files
echo "fdepulse.com" > site/CNAME
touch site/.nojekyll

# Generate external CSS
echo "  Generating CSS..."
python3 -c "import sys; sys.path.insert(0, 'scripts'); from templates import get_all_css; open('site/assets/css/styles.css', 'w').write(get_all_css())"

# Site generation
echo "  Generating homepage..."
python3 scripts/generate_homepage.py

echo "  Generating about page..."
python3 scripts/generate_about.py || true

echo "  Generating jobs page..."
python3 scripts/generate_jobs_page.py || true

echo "  Generating salaries page..."
python3 scripts/generate_salaries_page.py || true

echo "  Generating companies page..."
python3 scripts/generate_companies_page.py || true

echo "  Generating insights page..."
python3 scripts/generate_insights_page.py || true

echo "  Generating comparison pages..."
python3 scripts/generate_comparison_pages.py || true

echo "  Generating career index..."
python3 scripts/generate_career_index.py || true

echo "  Generating career pages..."
python3 scripts/generate_career_pages.py || true

echo "  Generating company profile pages..."
python3 scripts/generate_company_profile_pages.py || true

echo "  Generating additional comparison pages..."
python3 scripts/generate_more_comparisons.py || true

echo "  Generating location pages..."
python3 scripts/generate_location_pages.py || true

echo "  Generating long-tail career pages..."
python3 scripts/generate_longtail_career_pages.py || true

echo "  Generating additional company profiles..."
python3 scripts/generate_more_company_profiles.py || true

echo "  Generating additional location pages..."
python3 scripts/generate_more_locations.py || true

echo "  Generating topical pages..."
python3 scripts/generate_topical_pages.py || true

echo "  Generating top voices page..."
python3 scripts/generate_top_voices.py || true

# Finalization
echo "  Generating sitemap..."
python3 scripts/generate_sitemap.py || true

# Robots.txt
cat > site/robots.txt << 'ROBOTS'
User-agent: *
Allow: /
Sitemap: https://fdepulse.com/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GoogleOther
Allow: /
ROBOTS

FILE_COUNT=$(find site -type f | wc -l)
echo "=== FDE Pulse build complete: $FILE_COUNT files ==="
