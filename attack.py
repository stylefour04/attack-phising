import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== CONFIGURASI ===== #
MAX_THREADS = 20  # Lebih stabil untuk kebanyakan server
TIMEOUT = 8  # Timeout (detik) 
RETRY_COUNT = 2  # Jumlah percobaan ulang jika gagal

# ===== STYLE04 BANNER ===== #
def show_banner():
    print("""
    
                                   
    _  _____ _____  _    ____ _  __
   / \|_   _|_   _|/ \  / ___| |/ /
  / _ \ | |   | | / _ \| |   | ' / 
 / ___ \| |   | |/ ___ | |___| . \ 
/_/   \_|_|   |_/_/   \_\____|_|\_\
                                   


    >> STYLE04 ANTI-PHISHING SPAMMER <<
    >>  Guaranteed 90%+ Success Rate  <<
    """)

# ===== FUNGSI UTAMA ===== #
def generate_fake_data():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=16))
    return username, password

def send_request(url, data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Powered-By": "STYLE04-ANTI-PHISHING"
    }
    try:
        response = requests.post(url, data=data, headers=headers, timeout=TIMEOUT)
        return response.status_code
    except:
        return None

def spam_task(url, requests_count):
    success = 0
    for _ in range(requests_count):
        for attempt in range(RETRY_COUNT):
            username, password = generate_fake_data()
            data = {
                "username": username,
                "password": password,
                "submit": "login"
            }
            
            status = send_request(url, data)
            
            if status == 200:
                success += 1
                print(f"[✓] {username}:{password} -> Success")
                break
            elif attempt == RETRY_COUNT - 1:
                print(f"[×] {username}:{password} -> Failed (Attempts exhausted)")
            else:
                time.sleep(1)  # Delay sebelum retry
                
    return success

def main():
    show_banner()
    url = input("[?] Target URL (e.g. http://phishingsite.com): ").strip()
    total_requests = int(input("[?] Jumlah request (recommend 100-500): "))
    
    print("\n[!] Starting attack... (Ctrl+C to stop)")
    start_time = time.time()
    
    # Optimasi pembagian tugas
    chunk_size = min(50, max(10, total_requests // 5))
    chunks = [chunk_size] * (total_requests // chunk_size)
    if total_requests % chunk_size != 0:
        chunks.append(total_requests % chunk_size)
    
    total_success = 0
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(spam_task, url, chunk) for chunk in chunks]
        
        for future in as_completed(futures):
            total_success += future.result()
    
    # Hasil akhir
    duration = time.time() - start_time
    print(f"\n[+] Attack completed in {duration:.2f} seconds")
    print(f"[+] Success rate: {total_success}/{total_requests} ({total_success/total_requests*100:.1f}%)")
    print("[!] Laporkan phishing ke: https://reportphishing.id")

if __name__ == "__main__":
    main()
