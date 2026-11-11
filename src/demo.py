import requests
from bs4 import BeautifulSoup
from src.database import DatabaseRepository

url = "http://quotes.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

print(f"Отправляем запрос на {url}...")
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()


soup = BeautifulSoup(response.text, "lxml")
results = []

for quote_block in soup.select("div.quote"):
    text_element = quote_block.select_one("span.text")
    author_element = quote_block.select_one("small.author")
    
    if text_element and author_element:
        results.append({
            "id": len(results) + 1, 
            "name": author_element.get_text(strip=True),
            "message": text_element.get_text(strip=True)
        })

print(f"Успешно распарсено {len(results)} записей.")
print("Пример первой записи:", results[0] if results else "Нет данных")

db = DatabaseRepository(":memory:")
for item in results:
    db.add(item["id"], item["name"], item["message"])

print("\nДанные из БД (ID 1):")
print(db.get_by_id(1))

db.close()
