import requests
from urllib.parse import quote

WIKI_API_REST = "https://en.wikipedia.org/api/rest_v1/page/summary/"

def wiki_summary(topic: str) -> str:
    """
    Fetch a clean summary for a topic from Wikipedia.
    Handles disambiguation automatically if possible.
    """
    def fetch(title: str):
        url = WIKI_API_REST + quote(title.replace(" ", "_"))
        headers = {"User-Agent": "CrewAI-Lab/1.0"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return None
        return r.json()

    data = fetch(topic)
    if not data:
        return f"No summary found for '{topic}'."

    # Handle disambiguation
    if data.get("type") == "disambiguation":
        # Try picking the first link from the disambiguation page
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json"
        }
        r = requests.get(search_url, params=params)
        results = r.json().get("query", {}).get("search", [])
        if results:
            # Pick the first relevant page
            new_title = results[0]["title"]
            data = fetch(new_title)
            if data and data.get("extract"):
                return data["extract"]
        return f"The topic '{topic}' is ambiguous. See: {data['content_urls']['desktop']['page']}"

    return data.get("extract") or f"No summary available for '{topic}'."