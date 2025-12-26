import asyncio
import aiohttp
import time
import os
from datetime import datetime

# --- CONFIGURATION ---
PLAYLIST_DIR = 'playlists/'
OUTPUT_DIR = 'output/'
DELAY_THRESHOLD = 5000  # ms (5 seconds)
CONCURRENT_LIMIT = 50   # Max simultaneous checks

async def check_stream(session, name, url):
    """
    Checks a single stream URL for connectivity and latency.
    """
    start_time = time.time()
    try:
        # HEAD request is faster as it doesn't download the actual audio data
        async with session.head(url, timeout=10, allow_redirects=True) as response:
            latency = int((time.time() - start_time) * 1000)
            
            # Status codes below 400 are generally successful connections
            if response.status < 400:
                return {"name": name, "url": url, "latency": latency, "status": "Online"}
            else:
                return {"name": name, "url": url, "latency": latency, "status": f"Error {response.status}"}
    except Exception:
        return {"name": name, "url": url, "latency": 9999, "status": "Offline"}

async def process_playlist(file_path):
    """
    Reads a playlist file and extracts names and URLs.
    Supports basic M3U and simple TXT formats.
    """
    tasks = []
    # Professional User-Agent helps prevent blocks from hosting providers like radioca.st
    headers = {'User-Agent': 'StreamStabilityMonitor/1.0 (Broadcaster Quality Tool)'}
    
    # TCPConnector limit prevents your local machine from being flagged as a DoS attack
    connector = aiohttp.TCPConnector(limit=CONCURRENT_LIMIT)
    
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        current_name = "Unknown Station"
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if line.startswith("#EXTINF"):
                # Extracts station name from #EXTINF:0,Station Name
                current_name = line.split(',')[-1]
            elif not line.startswith("#"):
                tasks.append(check_stream(session, current_name, line))
        
        return await asyncio.gather(*tasks)

def save_results(results):
    """
    Filters online streams by latency and saves to a new M3U file in /output.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}verified_streams_{timestamp}.m3u"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        count = 0
        for r in results:
            if r['status'] == "Online" and r['latency'] <= DELAY_THRESHOLD:
                f.write(f"#EXTINF:-1,{r['name']} ({r['latency']}ms)\n")
                f.write(f"{r['url']}\n")
                count += 1
                
    print(f"✅ SUCCESS: {count} streams verified and saved to {filename}")

async def main():
    print("🚀 Stream Stability Monitor | Initializing...")
    
    if not os.path.exists(PLAYLIST_DIR):
        os.makedirs(PLAYLIST_DIR)
        print(f"Created '{PLAYLIST_DIR}' folder. Please add your .txt or .m3u files there.")
        return

    files = [f for f in os.listdir(PLAYLIST_DIR) if f.endswith(('.m3u', '.txt'))]
    
    if not files:
        print(f"No playlists found in {PLAYLIST_DIR}. Add a file (e.g., lbi.txt) to begin.")
        return

    for playlist in files:
        print(f"🔍 Checking: {playlist}...")
        results = await process_playlist(os.path.join(PLAYLIST_DIR, playlist))
        if results:
            save_results(results)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")
