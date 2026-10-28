import requests
from bs4 import BeautifulSoup


class ForumParser:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

    def parse_html(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        results = []
        for post in soup.select("div.post"):
            post_id = post.get("data-id")
            author = post.select_one(".author")
            message = post.select_one(".message")
            if post_id and author and message:
                results.append({
                    "id": int(post_id),
                    "name": author.get_text(strip=True),
                    "message": message.decode_contents().strip()
                })
        return results

    def parse_page(self, url: str) -> list[dict]:
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return self.parse_html(response.text)

    def save_to_db(self, parsed_data: list[dict], repository) -> int:
        for item in parsed_data:
            repository.add(item["id"], item["name"], item["message"])
        return len(parsed_data)
