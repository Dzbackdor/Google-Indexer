import os
import json
from pathlib import Path

def create_sample_files():
    """Buat file dan folder yang diperlukan"""
    
    # Buat folder structure
    folders = ['config/service-accounts', 'data', 'logs', 'src']
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {folder}")
    
    # Buat config file DENGAN SITEMAP_URL
    config_content = """domains:
  - domain: "https://vetcarepetshopconsult.com/"
    service_account: "config/service-accounts/website1-service-account.json"
    sitemap_url: "https://vetcarepetshopconsult.com/sitemap.xml"
    daily_quota: 200
"""
    with open('config/domains.yaml', 'w') as f:
        f.write(config_content)
    print("Created: config/domains.yaml")
    
    # Buat sample URLs file
    urls_content = """
    https://vetcarepetshopconsult.com/
    https://vetcarepetshopconsult.com/product/strategi-menang-di-slot-starlight-princess-mengenal-rtp-dan-pola-gacor
    https://vetcarepetshopconsult.com/product/temukan-kemenangan-besar-di-the-great-icescape-permainan-slot-online-yang-menawan
    https://vetcarepetshopconsult.com/product/turnamen-slot-terbesar-kesempatan-menang-besar
    """
    with open('data/urls_to_index.txt', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("Created: data/urls_to_index.txt")
    
    # Buat empty processed URLs file
    with open('data/processed_urls.txt', 'w', encoding='utf-8') as f:
        pass
    print("Created: data/processed_urls.txt")
    
    # Buat empty quota tracker
    with open('data/quota_tracker.json', 'w') as f:
        json.dump({}, f)
    print("Created: data/quota_tracker.json")
    
    print("\n✅ SEMUA FILE SUDAH DIBUAT!")
    print("📝 Selanjutnya:")
    print("1. Letakkan file Service Account JSON di: config/service-accounts/")
    print("2. Update nama file di config/domains.yaml jika perlu")
    print("3. Tambahkan URLs ke data/urls_to_index.txt")
    print("4. Jalankan: python src/main.py")

if __name__ == "__main__":
    create_sample_files()