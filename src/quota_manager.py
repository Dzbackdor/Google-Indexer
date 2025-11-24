import json
import datetime
from datetime import date
from collections import defaultdict
import os

class QuotaManager:
    def __init__(self, quota_file='data/quota_tracker.json'):
        # Buat folder data jika belum ada
        os.makedirs('data', exist_ok=True)
        
        self.quota_file = quota_file
        self.daily_quota = 200
        self.usage = self.load_usage()
    
    def load_usage(self):
        """Load usage data dari file"""
        try:
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
                # Convert ke defaultdict untuk handle missing keys
                return defaultdict(lambda: {
                    'used_today': 0,
                    'last_reset': str(date.today()),
                    'total_used': 0
                }, data)
        except (FileNotFoundError, json.JSONDecodeError):
            return defaultdict(lambda: {
                'used_today': 0,
                'last_reset': str(date.today()),
                'total_used': 0
            })
    
    def save_usage(self):
        """Simpan usage data ke file"""
        try:
            # Convert defaultdict ke regular dict sebelum save
            with open(self.quota_file, 'w') as f:
                json.dump(dict(self.usage), f, indent=2)
        except Exception as e:
            print(f"Error saving quota data: {e}")
    
    def check_quota(self, domain):
        """Cek apakah domain masih ada quota tersisa"""
        self.reset_if_new_day(domain)
        
        used_today = self.usage[domain]['used_today']
        remaining = self.daily_quota - used_today
        
        print(f"Quota check for {domain}: {used_today}/{self.daily_quota} (remaining: {remaining})")
        
        return remaining > 0, remaining
    
    def reset_if_new_day(self, domain):
        """Reset counter jika sudah hari baru"""
        today = str(date.today())
        last_reset = self.usage[domain].get('last_reset', '')
        
        if last_reset != today:
            self.usage[domain]['used_today'] = 0
            self.usage[domain]['last_reset'] = today
            print(f"RESET: Quota for {domain} - new day: {today}")
            self.save_usage()
    
    def mark_used(self, domain, count=1):
        """Tandai bahwa quota telah digunakan"""
        self.reset_if_new_day(domain)
        
        # Pastikan domain ada di usage
        if domain not in self.usage:
            self.usage[domain] = {
                'used_today': 0,
                'last_reset': str(date.today()),
                'total_used': 0
            }
        
        self.usage[domain]['used_today'] += count
        self.usage[domain]['total_used'] += count
        self.save_usage()
        
        print(f"USED: {count} for {domain}. Total today: {self.usage[domain]['used_today']}")
    
    def get_usage_report(self):
        """Generate laporan penggunaan quota"""
        report = {}
        for domain, data in dict(self.usage).items():  # Convert ke dict
            remaining = self.daily_quota - data['used_today']
            report[domain] = {
                'used_today': data['used_today'],
                'remaining_today': remaining,
                'total_used': data['total_used'],
                'last_reset': data['last_reset']
            }
        return report