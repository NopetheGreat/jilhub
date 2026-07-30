from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import random
import re
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

if os.path.exists("category.txt"):
    with open("category.txt", "r", encoding="utf-8") as f:
        all_categories = [line.strip() for line in f if line.strip()]
    
    # Pick up to 1000 categories randomly every 24-hour cycle
    target_count = min(1000, len(all_categories))
    if target_count > 0:
        categories = random.sample(all_categories, target_count)
    else:
        categories = []
else:
    categories = []

if not categories:
    print("No categories found.")
    exit()

session = requests.Session()
session.headers.update(headers)

def fetch_category_page(args):
    base_url, page_num = args
    cat_name = base_url.rstrip("/").split("/")[-1].replace("-", " ").title()
    url = f"{base_url.rstrip('/')}/{page_num}/" if page_num > 1 else base_url
    
    local_tasks = []
    try:
        response = session.get(url, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            video_items = soup.find_all("a", href=True)
            for item in video_items:
                title_el = item.find("strong", class_="title")
                duration_el = item.find("div", class_="duration")
                if title_el and duration_el:
                    page_url = item["href"]
                    if not page_url.startswith("http"):
                        domain = "/".join(base_url.split("/")[:3])
                        page_url = domain + page_url

                    title = title_el.get_text(strip=True)
                    img_el = item.find("img", class_="thumb")
                    thumbnail = img_el.get("data-original") or img_el.get("src", "") if img_el else ""
                    quality = item.find("span", class_="is-hd").get_text(strip=True) if item.find("span", class_="is-hd") else "Standard"
                    rating = item.find("div", class_="rating").get_text(strip=True) if item.find("div", class_="rating") else "N/A"
                    added = item.find("div", class_="added").get_text(strip=True) if item.find("div", class_="added") else "N/A"
                    views = item.find("div", class_="views").get_text(strip=True) if item.find("div", class_="views") else "0"
                    duration = duration_el.get_text(strip=True)

                    local_tasks.append((page_url, title, thumbnail, quality, duration, rating, added, views, cat_name))
    except:
        pass
    return local_tasks

cat_page_args = [(cat, page) for cat in categories for page in range(1, 4)]
tasks = []
processed_video_urls = set()

print(f"Scraping category pages concurrently...")
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = [executor.submit(fetch_category_page, arg) for arg in cat_page_args]
    for future in as_completed(futures):
        for task in future.result():
            p_url = task[0]
            if p_url not in processed_video_urls:
                processed_video_urls.add(p_url)
                tasks.append(task)

print(f"Collected {len(tasks)} unique videos. Fetching sources...")

def fetch_video(task):
    p_url, title, thumb, qual, dur, rat, add, view, cat = task
    try:
        page_res = session.get(p_url, timeout=3)
        if page_res.status_code == 200:
            match = re.search(r'https?://[^\s<>"\']+?/contents/videos/[^\s<>"\']+\.mp4', page_res.text)
            if not match:
                match = re.search(r'https?://[^\s<>"\']+?/get_file/[^\s<>"\']+\.mp4', page_res.text)
            if match:
                return {
                    "url": match.group(0),
                    "title": title,
                    "thumbnail": thumb,
                    "quality": qual,
                    "duration": dur,
                    "rating": rat,
                    "added": add,
                    "views": view,
                    "category": cat
                }
    except:
        pass
    return None

videos_data = []
total_tasks = len(tasks)
completed_count = 0

with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(fetch_video, t): t for t in tasks}
    for future in as_completed(futures):
        res = future.result()
        if res:
            videos_data.append(res)
        completed_count += 1
        print(f"Progress: {completed_count}/{total_tasks}", end="\r", flush=True)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(videos_data, f, indent=4)

print(f"\nDone: Saved {len(videos_data)} records to data.json")