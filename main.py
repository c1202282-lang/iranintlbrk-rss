import requests
from bs4 import BeautifulSoup
import datetime
import xml.dom.minidom

# List of data sources (priority order)
SOURCES = [
    "https://nitter.net/IranIntlbrk",  # Main source
    "https://webcache.googleusercontent.com/search?q=site:x.com/IranIntlbrk",  # Google cache
    "https://web.archive.org/web/https://x.com/IranIntlbrk"  # Web Archive
]

def fetch_from_source(url):
    """Fetch tweets from a specific source URL"""
    try:
        print(f"Trying source: {url}")
        html = requests.get(url, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
        tweets = []
        
        # Nitter parsing
        if "nitter" in url:
            items = soup.select(".timeline-item")
            for it in items:
                content = it.select_one(".tweet-content")
                date_tag = it.select_one(".tweet-date a")
                if content and date_tag:
                    text = content.get_text(strip=True)
                    link = "https://x.com" + date_tag["href"]
                    tweets.append((text, link))
        else:
            # Fallback: Google Cache or Web Archive (less structured)
            paragraphs = soup.find_all("p")
            for p in paragraphs[:10]:
                text = p.get_text(strip=True)
                link = url
                if len(text) > 20:
                    tweets.append((text, link))
        
        return tweets
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def get_latest_tweets():
    """Try each source until tweets are found"""
    for src in SOURCES:
        tweets = fetch_from_source(src)
        if tweets:
            print(f"Got {len(tweets)} tweets from {src}")
            return tweets
    return []

def build_rss(tweets):
    """Generate RSS XML file from list of tweets"""
    from xml.etree.ElementTree import Element, SubElement, tostring
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "IranIntlbrk RSS (Anti-Block)"
    SubElement(channel, "link").text = "https://x.com/IranIntlbrk"
    SubElement(channel, "description").text = "Latest tweets without VPN"

    now = datetime.datetime.utcnow()
    for text, link in tweets:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = text[:50] + "..."
        SubElement(item, "link").text = link
        SubElement(item, "description").text = text
        SubElement(item, "pubDate").text = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    xml_str = xml.dom.minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

if __name__ == "__main__":
    tweets = get_latest_tweets()
    build_rss(tweets)
