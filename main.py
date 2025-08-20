from datetime import datetime
import os

# آیتم‌های تستی
items = [
    {
        "title": "Test News 1",
        "link": "https://example.com/1",
        "description": "This is a test item for IranIntlbrk RSS.",
        "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    },
    {
        "title": "Test News 2",
        "link": "https://example.com/2",
        "description": "Second test item for IranIntlbrk RSS.",
        "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }
]

# تولید رشته‌ی XML RSS
rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>IranIntlbrk RSS (Anti-Block)</title>
<link>https://x.com/IranIntlbrk</link>
<description>Latest tweets without VPN</description>
"""

for item in items:
    rss_content += f"""<item>
<title>{item['title']}</title>
<link>{item['link']}</link>
<description>{item['description']}</description>
<pubDate>{item['pubDate']}</pubDate>
</item>
"""

rss_content += """
</channel>
</rss>
"""

# ساخت پوشه خروجی و ذخیره در آن
os.makedirs("output", exist_ok=True)
with open("output/feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_content)

print("feed.xml created successfully in /output with test items.")
