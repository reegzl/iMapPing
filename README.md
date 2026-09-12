<p align="center">
  <pre align="center">
██╗███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
██║████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
██║██╔████╔██║███████║██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗
██║██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██║██║╚██╗██║██║   ██║
██║██║ ╚═╝ ██║██║  ██║██║     ██║     ██║██║ ╚████║╚██████╔╝
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝ ╚══════╝ 
  </pre>
</p>

<p align="center">
  <b>An advanced, colored multi-threaded CLI utility for high-concurrency IMAP server connectivity testing, SSL handshake verification, and automatic dead-domain purging. Created by REEGZL.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-blue?style=flat-square" alt="Platform Cross-Platform">
  <img src="https://img.shields.io/badge/Language-Python-yellow?style=flat-square" alt="Language Python">
  <img src="https://img.shields.io/badge/Version-v1.0-orange?style=flat-square" alt="Version v1.0">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License MIT">
</p>

---

## Overview

**iMapPing** is a high-performance terminal utility built in Python by **REEGZL**, designed to validate massive lists of IMAP server routing rules instantly. When dealing with large domain lists (such as thousands or millions of educational and corporate mail servers), checking them manually or via active authentication risks account lockouts and IP blacklisting. 

iMapPing bypasses credential checking entirely, performing ultra-fast, non-invasive network-level socket checks and SSL handshakes concurrently to separate functional servers from dead wood.

---

## Features

* **High-Concurrency Threading:** Utilizes a `ThreadPoolExecutor` running 100 concurrent worker threads to test large datasets in minutes instead of days.
* **Safe, Non-Invasive Testing:** Strictly evaluates raw TCP connectivity and SSL/TLS handshakes without sending authentication payloads, completely eliminating account locks or auth blockages.
* **Real-Time Colored UI & Progress Bar:** Features a dynamic terminal progress interface displaying percentage completion, active thread counts, live working servers, and non-working servers.
* **Automated Result Splitting:** Automatically parses and partitions data into `domains_working.txt` (keeping valid routes) and `domains_dead.txt` (isolating dead configurations).
* **Lightweight & Standalone:** Built using Python's native standard library (`socket`, `ssl`, `concurrent.futures`), requiring no external pip packages.

---

## How It Works

iMapPing acts as an automated network health check for mail routing infrastructure:
1. **File Ingestion:** Reads the target configurations line by line from `domains.txt`, interpreting custom domain, host, and port pairings.
2. **Socket & SSL Handshake:** Spawns background worker threads that open a raw network socket to the mail host and securely negotiate the TLS/SSL wrapper (with certificate verification relaxed to accommodate self-signed institutional servers).
3. **Data Partitioning:** Safely tracks metrics using thread-safe locking mechanisms, rewriting operational nodes back to disk while cleanly cataloging dead targets.

---

## Getting Started

### Prerequisites
* Python 3.8 or higher installed on your system.

### Installation & Usage

1. Clone the repository or download the script:
```bash
   git clone [https://github.com/reegzl/iMapPing.git](https://github.com/reegzl/iMapPing.git)
```
2. Navigate into the directory containing iMapPing.py.
3. Ensure your target domain routes are formatted inside a domains.txt file in the same directory (using domain | host | port format).
4. Run the script:
```bash
   python iMapPing.py
```

---

## Support the Developer

If iMapPing has streamlined your workflow or saved you time, consider supporting its development with crypto:

Bitcoin (BTC): `bc1qm427zm2jxmesulwjd4j95k82ck9h7l9n7wqemt`

Ethereum (ETH): `0xf6bf5446Efe20f1404016895c6deaf0F22EF76CE`

Stellar (XLM): `GBDLBCAE75FO3QNB5VWCWMEOIV2GEP7UFPP3CQICPM3KOZ2YVY55E7OJ`

Thanks for checking out the tool!
