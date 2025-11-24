import os

class URLManager:
    def __init__(self):
        # Buat folder data jika belum ada
        os.makedirs('data', exist_ok=True)
        self.processed_urls = self.load_processed_urls()
    
    def load_processed_urls(self):
        """Load daftar URL yang sudah diproses"""
        try:
            processed_file = 'data/processed_urls.txt'
            if os.path.exists(processed_file):
                with open(processed_file, 'r', encoding='utf-8') as f:
                    return set(line.strip() for line in f if line.strip())
            else:
                # Buat file kosong jika belum ada
                with open(processed_file, 'w', encoding='utf-8') as f:
                    pass
                return set()
        except Exception as e:
            print(f"Error loading processed URLs: {e}")
            return set()
    
    def save_processed_urls(self):
        """Simpan daftar URL yang sudah diproses"""
        try:
            with open('data/processed_urls.txt', 'w', encoding='utf-8') as f:
                for url in self.processed_urls:
                    f.write(url + '\n')
        except Exception as e:
            print(f"Error saving processed URLs: {e}")
    
    def load_urls_from_txt(self, txt_file, domain_filter=None):
        """Load URLs dari TXT file"""
        try:
            if not os.path.exists(txt_file):
                print(f"File {txt_file} tidak ditemukan")
                return []
            
            urls = []
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):  # Skip empty lines dan comments
                        if self.is_valid_url(url) and url not in self.processed_urls:
                            if domain_filter is None or domain_filter in url:
                                urls.append(url)
            
            print(f"Loaded {len(urls)} URLs from {txt_file}")
            return urls
            
        except Exception as e:
            print(f"Error loading URLs from TXT: {e}")
            return []
    
    def is_valid_url(self, url):
        """Validasi URL format"""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def mark_as_processed(self, url):
        """Tandai URL sebagai sudah diproses"""
        self.processed_urls.add(url)
        self.save_processed_urls()
    
    def get_domain_from_url(self, url):
        """Extract domain dari URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except Exception:
            return None