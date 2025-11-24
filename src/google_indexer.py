import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os
import time

class GoogleIndexer:
    def __init__(self, service_account_file, domain):
        self.service_account_file = service_account_file
        self.domain = domain
        self.credentials = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate dengan Google Service Account"""
        try:
            SCOPES = ['https://www.googleapis.com/auth/indexing']
            
            self.credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=SCOPES)
            
            # Refresh token pertama kali
            self.credentials.refresh(Request())
            
            print(f"SUCCESS: Authenticated for {self.domain}")
            return True
            
        except Exception as e:
            print(f"ERROR: Authentication failed for {self.domain}: {str(e)}")
            return False
    
    def submit_url_sync(self, url):
        """Submit single URL (synchronous version)"""
        try:
            # Refresh token jika expired
            if not self.credentials or self.credentials.expired:
                print("Refreshing token...")
                self.authenticate()
            
            endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
            
            payload = {
                'url': url,
                'type': 'URL_UPDATED'
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.credentials.token}'
            }
            
            response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                print(f"SUCCESS: Indexed - {url}")
                return {
                    'url': url,
                    'status': 'success',
                    'response': response.json()
                }
            else:
                print(f"FAILED: {url} - {response.status_code}")
                # Coba refresh token dan coba sekali lagi
                if response.status_code == 401:
                    print("Token expired, refreshing...")
                    self.authenticate()
                    
                    # Coba lagi dengan token baru
                    headers['Authorization'] = f'Bearer {self.credentials.token}'
                    response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
                    
                    if response.status_code == 200:
                        print(f"SUCCESS (retry): Indexed - {url}")
                        return {
                            'url': url,
                            'status': 'success',
                            'response': response.json()
                        }
                
                print(f"Error details: {response.text}")
                return {
                    'url': url,
                    'status': 'error',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"ERROR: {url} - {str(e)}")
            return {
                'url': url,
                'status': 'error', 
                'error': str(e)
            }