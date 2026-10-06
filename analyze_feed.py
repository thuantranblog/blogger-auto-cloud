import urllib.request
import json

url = "https://www.luviet.com/feeds/posts/default?alt=json&max-results=100"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    
    entries = data.get("feed", {}).get("entry", [])
    print(f"Total posts: {len(entries)}")
    with open("all_posts_clean.txt", "w", encoding="utf-8") as out:
        for i, e in enumerate(entries, 1):
            title = e.get("title", {}).get("$t", "")
            pub = e.get("published", {}).get("$t", "")[:10]
            cats = [c.get("term", "") for c in e.get("category", [])]
            link = next((l.get("href") for l in e.get("link", []) if l.get("rel") == "alternate"), "")
            out.write(f"{i}. [{pub}] {title}\n   Link: {link}\n   Labels: {', '.join(cats)}\n")
    print("Exported to all_posts_clean.txt")
except Exception as ex:
    print("Error:", ex)
