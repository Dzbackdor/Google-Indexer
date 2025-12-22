# Google Indexer

Automation tool untuk submit URL ke **Google Indexing API** secara massal. Mendukung multiple domains dengan quota 200 URL/hari.
---

## 🔑 CARA MENDAPATKAN SERVICE ACCOUNT

### **Langkah 1: Buat Project di Google Cloud Console**

1. Buka **Google Cloud Console**
2. Klik **Select Project → New Project**
3. Beri nama: **Google-Indexer-API**
4. Klik **Create**

### **Langkah 2: Aktifkan Google Indexing API**

1. Sidebar: **APIs & Services → Library**
2. Cari "**Indexing API**"
3. Klik **Google Indexing API → Enable**

### **Langkah 3: Buat Service Account**

1. Masuk ke: **APIs & Services → Credentials**
2. Klik **Create Credentials → Service Account**
3. Isi:

   * Name: `google-indexer-bot`
   * Description: *For submitting URLs to Google Indexing API*
4. Klik **Create and Continue**
5. Role: pilih **Basic → Viewer**
6. Klik **Done**

### **Langkah 4: Download JSON Key**

1. Klik service account: **google-indexer-bot**
2. Tab **Keys → Add Key → Create New Key**
3. Pilih **JSON → Create**
4. File JSON otomatis terdownload

### **Langkah 5: Tambahkan ke Google Search Console**

1. Buka **Google Search Console**
2. Pilih property yang ingin ditambahkan
3. Masuk: **Settings → Users and permissions**
4. Klik **Add User** dan masukkan email service account:

```
google-indexer-bot@PROJECT-NAME.iam.gserviceaccount.com
```

5. Pilih permission **Owner**
6. Klik **Add**

---

## 📁 STRUKTUR FOLDER SETELAH DAPAT JSON

```
google-indexer/
├── config/
│   ├── domains.yaml
│   └── service-accounts/
│       └── website1-service-account.json
├── data/
│   ├── urls_to_index.txt
│   ├── processed_urls.txt
│   └── quota_tracker.json
├── logs/
└── src/
    ├── __init__.py
    ├── google_indexer.py
    ├── quota_manager.py
    ├── url_manager.py
    └── main.py
```

---

## 🔧 CARA MASUKKAN KE CODE

### **📁 1. Update: `config/domains.yaml`**

```yaml
domains:
  - domain: "https://website-pertama.com/"
    service_account: "config/service-accounts/website1-service-account.json"
    sitemap_url: "https://website-pertama.com/sitemap.xml"
    daily_quota: 200

  - domain: "https://website-kedua.com/"
    service_account: "config/service-accounts/website2-service-account.json"
    sitemap_url: "https://website-kedua.com/sitemap.xml"
    daily_quota: 200
```

### **📁 2. Letakkan File JSON di Folder yang Benar**

Simpan semua file ke:

```
config/service-accounts/
```

Contoh rename:

```
website1-service-account.json
website2-service-account.json
```

### **📁 3. Contoh Isi File Service Account JSON**

```json
{
  "type": "service_account",
  "project_id": "your-project-name-123456",
  "private_key_id": "a1b2c3d4e5f6g7h8i9j0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCw...\n-----END PRIVATE KEY-----\n",
  "client_email": "google-indexer-bot@your-project-name-123456.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-indexer-bot%40your-project-name-123456.iam.gserviceaccount.com"
}
```

---

## 🚀 CARA MENJALANKAN

### **1. Install dependencies**

```
pip install -r requirements.txt
```

### **2. Test Akses**

```
python test_access.py
```

### **3. Jalankan Program**

```
python src/main.py
```

---

