from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import json

def test_with_correct_scope():
    SERVICE_ACCOUNT_FILE = 'config/service-accounts/website1-service-account.json'
    TEST_URL = "https://vetcarepetshopconsult.com/"
    
    try:
        # SCOPE YANG BENAR UNTUK INDEXING API
        SCOPES = ['https://www.googleapis.com/auth/indexing']
        
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        credentials.refresh(Request())
        
        print("✅ Authentication SUCCESS")
        print(f"Service Account: {credentials.service_account_email}")
        print(f"Scopes: {credentials.scopes}")
        print(f"Token (first 50 chars): {credentials.token[:50]}...")
        
        # Test Indexing API
        endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
        payload = {
            'url': TEST_URL,
            'type': 'URL_UPDATED'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {credentials.token}'
        }
        
        print(f"\n🔍 Testing Indexing API with: {TEST_URL}")
        
        response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! URL submitted to Google Indexing API")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            error_data = response.json()
            print(f"Error: {json.dumps(error_data, indent=2)}")
            
            # Specific error analysis
            error_msg = error_data.get('error', {}).get('message', '')
            if 'forbidden' in error_msg.lower() or 'permission' in error_msg.lower():
                print("\n🔒 PERMISSION ISSUE DETECTED")
                print("Possible causes:")
                print("1. Service Account not added to Search Console")
                print("2. Wrong permission level (need 'Owner')")
                print("3. Domain not verified in Search Console")
                print("4. Service Account email typo")
                
            return False
            
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    test_with_correct_scope()