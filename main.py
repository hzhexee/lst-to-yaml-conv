import requests
import yaml

LST_URL = "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/geoblock.lst"
OUTPUT_YAML = "output.yaml"

def fetch_lst(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_domains(lst_text):
    domains = []
    for line in lst_text.strip().splitlines():
        line = line.strip()
        if line:
            domains.append(f'+.{line}')
    return {"payload": domains}

def save_as_yaml(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

def main():
    lst_content = fetch_lst(LST_URL)
    parsed_data = parse_domains(lst_content)
    save_as_yaml(parsed_data, OUTPUT_YAML)

if __name__ == "__main__":
    main()
