<pre>

📡 Stream Stability Monitor
A high-performance, asynchronous stream health validator designed for professional broadcasters.

Originally forked from AlexKwan1981, this version has been modernized for the 2025 broadcast landscape with English localization, HTTPS/TLS support, and optimized latency detection.

🚀 Key Features
Parallel Asynchronous Checking: Uses aiohttp to check hundreds of streams simultaneously, minimizing total execution time.

Smart Latency Thresholds: Categorizes stream health based on custom millisecond response times.

Broadcaster-Grade Validation: Specifically optimized for ICY (Shoutcast/Icecast) and HLS (m3u8) endpoints.

Automated M3U Generation: Outputs timestamped, high-quality playlists containing only verified, low-latency links.

English Localization: Fully translated UI and console logging for global dev teams.

🛠️ Installation & Setup
Requires Python 3.10+ for modern asyncio support.

Clone the repository:

Bash

git clone [https://github.com/YourUsername/stream-stability-monitor.git](https://github.com/YourUsername/stream-stability-monitor.git)
cd stream-stability-monitor
Install dependencies:

Bash

pip install -r requirements.txt
📈 Usage
Place your .m3u or .txt source files in the /playlists directory, then run:

Bash

python main.py
Results will be generated in the /output folder, filtered by your delay_threshold (default: 5000ms).

🌍 About the Author
Maintained by the technical lead of lbi Radio Lebanon. This tool is part of our commitment to ensuring 99.9% stream availability and low-latency delivery for our listeners worldwide.

⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details. </pre>
