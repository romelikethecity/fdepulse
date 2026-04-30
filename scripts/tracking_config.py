#!/usr/bin/env python3
"""
Analytics Configuration for FDE Pulse
"""

# Google Analytics 4 — set after creating GA4 property
GA4_MEASUREMENT_ID = "G-KSEW9N2N0M"

# Microsoft Clarity — set after creating Clarity project
CLARITY_PROJECT_ID = ""


def get_tracking_code():
    """Returns the tracking code snippet to add to <head>"""
    code = ""

    if GA4_MEASUREMENT_ID:
        code += f'''
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA4_MEASUREMENT_ID}');
    </script>
'''

    if CLARITY_PROJECT_ID:
        code += f'''
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{CLARITY_PROJECT_ID}");
    </script>
'''

    if GA4_MEASUREMENT_ID:
        code += '''
    <!-- GA4 Custom Events -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Track newsletter CTA clicks
            document.querySelectorAll('.cta-box .btn, .btn-subscribe').forEach(function(el) {
                el.addEventListener('click', function() {
                    gtag('event', 'cta_click', {
                        event_category: 'newsletter',
                        event_label: el.textContent.trim()
                    });
                });
            });

            // Track job card clicks
            document.querySelectorAll('.job-card').forEach(function(el) {
                el.addEventListener('click', function() {
                    var title = el.querySelector('.job-card__title');
                    gtag('event', 'job_click', {
                        event_category: 'jobs',
                        event_label: title ? title.textContent.trim() : 'unknown'
                    });
                });
            });

            // Track outbound job application clicks
            document.querySelectorAll('a[href*="linkedin.com"], a[href*="greenhouse.io"], a[href*="lever.co"], a[href*="workday.com"]').forEach(function(el) {
                el.addEventListener('click', function() {
                    gtag('event', 'outbound_click', {
                        event_category: 'job_apply',
                        event_label: el.href
                    });
                });
            });

            // Page type classification
            var path = window.location.pathname;
            var pageType = 'other';
            if (path === '/') pageType = 'homepage';
            else if (path.startsWith('/jobs/')) pageType = 'jobs';
            else if (path.startsWith('/salaries/')) pageType = 'salaries';
            else if (path.startsWith('/companies/')) pageType = 'companies';
            else if (path.startsWith('/insights/')) pageType = 'insights';
            else if (path.startsWith('/about')) pageType = 'about';
            gtag('set', 'user_properties', { page_type: pageType });

            // Scroll depth tracking
            var scrollMarks = {25: false, 50: false, 75: false, 100: false};
            window.addEventListener('scroll', function() {
                var scrollPct = Math.round((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100);
                [25, 50, 75, 100].forEach(function(mark) {
                    if (scrollPct >= mark && !scrollMarks[mark]) {
                        scrollMarks[mark] = true;
                        gtag('event', 'scroll_depth', {
                            event_category: 'engagement',
                            event_label: mark + '%',
                            page_type: pageType
                        });
                    }
                });
            });
        });
    </script>
'''

    return code
