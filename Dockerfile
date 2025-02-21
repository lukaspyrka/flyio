# Pobierz oficjalny obraz Pythona 3.12
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip
RUN python -m playwright install
RUN pip install --upgrade playwright

# Instalacja Playwright + dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libnss3 libatk1.0-0 libx11-xcb1 libxcb-dri3-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libxcursor1

RUN playwright install-deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
