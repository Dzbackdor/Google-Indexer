import yaml
import json
from datetime import datetime
from google_indexer import GoogleIndexer
from quota_manager import QuotaManager
from url_manager import URLManager
import os
import time  # Tambahkan ini

class BulkIndexer:
    def __init__(self, config_path='config/domains.yaml'):
        os.makedirs('logs', exist_ok=True)
        self.config = self.load_config(config_path)
        self.quota_manager = QuotaManager()
        self.url_manager = URLManager()
        self.indexers = {}
        self.initialize_indexers()
    
    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                print(f"Loaded config: {len(config.get('domains', []))} domains")
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {'domains': []}
    
    def initialize_indexers(self):
        for domain_config in self.config['domains']:
            domain = domain_config['domain']
            service_account = domain_config['service_account']
            
            if not os.path.exists(service_account):
                print(f"ERROR: Service account file not found: {service_account}")
                continue
                
            try:
                self.indexers[domain] = GoogleIndexer(
                    service_account_file=service_account,
                    domain=domain
                )
                print(f"Initialized indexer for: {domain}")
            except Exception as e:
                print(f"ERROR: Failed to initialize indexer for {domain}: {e}")
    
    def process_domain_sync(self, domain, urls):
        try:
            if domain not in self.indexers:
                print(f"ERROR: No indexer found for {domain}")
                return []
                
            indexer = self.indexers[domain]
            results = []
            
            has_quota, remaining = self.quota_manager.check_quota(domain)
            if not has_quota:
                print(f"NO QUOTA: No quota remaining for {domain}")
                return results
            
            urls_to_process = urls[:remaining]
            print(f"PROCESSING: {len(urls_to_process)} URLs for {domain}")
            
            success_count = 0
            for i, url in enumerate(urls_to_process, 1):
                print(f"Progress: {i}/{len(urls_to_process)}")
                
                result = indexer.submit_url_sync(url)
                results.append(result)
                
                if result['status'] == 'success':
                    self.quota_manager.mark_used(domain)
                    self.url_manager.mark_as_processed(url)
                    success_count += 1
                
                # Tambahkan delay 1 detik antara requests
                if i < len(urls_to_process):
                    time.sleep(1)
            
            print(f"COMPLETED: {success_count}/{len(urls_to_process)} successful for {domain}")
            return results
            
        except Exception as e:
            print(f"ERROR in process_domain_sync for {domain}: {e}")
            return []
    
    def process_all_domains_sync(self, url_source='data/urls_to_index.txt'):
        print("STARTING: Bulk indexing process")
        
        all_results = {}
        
        for domain_config in self.config['domains']:
            domain = domain_config['domain']
            
            urls = self.url_manager.load_urls_from_txt(url_source, domain_filter=domain)
            
            if urls:
                print(f"Found {len(urls)} URLs for {domain}")
                results = self.process_domain_sync(domain, urls)
                all_results[domain] = results
            else:
                print(f"WARNING: No URLs found for {domain}")
        
        return self.generate_report(all_results)
    
    def generate_report(self, all_results):
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'summary': {},
                'details': all_results,
                'quota_usage': self.quota_manager.get_usage_report()
            }
            
            total_success = 0
            total_failed = 0
            
            for domain, results in all_results.items():
                success_count = sum(1 for r in results if r.get('status') == 'success')
                failed_count = sum(1 for r in results if r.get('status') == 'error')
                
                total_success += success_count
                total_failed += failed_count
                
                report['summary'][domain] = {
                    'success': success_count,
                    'failed': failed_count,
                    'total_processed': len(results)
                }
            
            report['summary']['total'] = {
                'success': total_success,
                'failed': total_failed,
                'total_processed': total_success + total_failed
            }
            
            report_file = f"logs/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📊 FINAL REPORT:")
            print(f"   Success: {total_success}")
            print(f"   Failed: {total_failed}")
            print(f"   Total: {total_success + total_failed}")
            print(f"   Report saved to: {report_file}")
            
            return report
            
        except Exception as e:
            print(f"ERROR generating report: {e}")
            return {}

def main():
    try:
        indexer = BulkIndexer()
        results = indexer.process_all_domains_sync()
        print("\n🎉 Processing completed!")
        return results
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return None

if __name__ == "__main__":
    main()