import os
import requests
import gc
import traceback
import time
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.DEBUG)
url = "https://www.viewstats.com/@mrbeast/channelytics"



def get_view_count(url):
    with sync_playwright() as p:
        # Uruchomienie przeglądarki w trybie headless
        browser = p.chromium.launch(
            headless=True,
        )
        page = browser.new_page()
        # Załaduj stronę
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(5)
        # Poczekaj na obecność elementów z klasą "view-count"
        try:
            page.locator(".view-count").first.wait_for(timeout=30000)  # 30s zamiast 300s
        except Exception as e:
            print(f"Błąd Playwright: {e}")
        if not page.locator(".view-count").first.is_visible():
            browser.close()
            return "nie znaleziono"

        page.wait_for_selector(".view-count", timeout=300000)
        
        # Pobierz tekst z pierwszego elementu "view-count"
        view_count = page.locator(".view-count").first.inner_text()
        
        # Zamknięcie przeglądarki
        browser.close()
        gc.collect()
        return view_count

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Działa!"})

@app.route("/send-data", methods=["POST"])
def receive_data():
    data = request.json
    if not data or "url" not in data:
        return jsonify({"error": "Brak URL w żądaniu"}), 400  # Zwraca kod błędu 400

    url = data["url"]
    if not url.startswith("http"):
        return jsonify({"error": "Niepoprawny URL"}), 400
    view_count = get_view_count(url)
    return jsonify({"status": "success", "view_count": view_count})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
