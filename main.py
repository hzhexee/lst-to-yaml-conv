import requests
import yaml
import os
from urllib.parse import urlparse

# Список URL-ов для конвертации
LST_URLS = [
    "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/geoblock.lst",
    # Добавьте здесь другие ссылки
]

def fetch_lst(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_domains(lst_text):
    domains = []
    for line in lst_text.strip().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            domains.append(f'+.{line}')
    return {"payload": domains}

def save_as_yaml(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

def get_filename_from_url(url):
    # Извлекаем имя файла из URL
    path = urlparse(url).path
    filename = os.path.basename(path)
    
    # Убираем расширение .lst если оно есть
    if filename.endswith('.lst'):
        filename = filename[:-4]
    
    return f"{filename}.yaml"

def main():
    for url in LST_URLS:
        try:
            print(f"Обработка {url}...")
            lst_content = fetch_lst(url)
            parsed_data = parse_domains(lst_content)
            output_filename = get_filename_from_url(url)
            save_as_yaml(parsed_data, output_filename)
            print(f"Готово: {output_filename}")
        except Exception as e:
            print(f"Ошибка при обработке {url}: {e}")

if __name__ == "__main__":
    main()
