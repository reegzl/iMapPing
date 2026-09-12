import os
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

BANNER = """\033[35m
██╗███╗   ███╗ █████╗ ██████╗   ██████╗ ██╗███╗   ██╗ ██████╗ 
╚═╝████╗ ████║██╔══██╗██╔══██╗  ██╔══██╗██║████╗  ██║██╔════╝ 
██║██╔████╔██║███████║██████╔╝  ██████╔╝██║██╔██╗ ██║██║  ███╗
██║██║╚██╔╝██║██╔══██║██╔═══╝   ██╔═══╝ ██║██║╚██╗██║██║   ██║
██║██║ ╚═╝ ██║██║  ██║██║       ██║     ██║██║ ╚████║╚██████╔╝
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝ ╚══════╝ 
\033[0m"""

def test_single_domain(line):
    stripped = line.strip()
    if not stripped or stripped.startswith('#') or '|' not in stripped:
        return (line, True, None, True)
    
    parts = stripped.split('|')
    domain = parts[0].strip()
    host = parts[1].strip()
    port = int(parts[2].strip()) if len(parts) > 2 and parts[2].strip().isdigit() else 993

    is_alive = False
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((host, port), timeout=3) as sock:
            if port == 993:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    is_alive = True
            else:
                is_alive = True
    except Exception:
        is_alive = False

    return (line, is_alive, domain, False)

def test_domains(domains_file="domains.txt", output_working="domains_working.txt", output_dead="domains_dead.txt"):
    print(BANNER)

    if not os.path.exists(domains_file):
        print("\033[31m[ERROR] 'domains.txt' not found.\033[0m")
        return

    with open(domains_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_lines = len(lines)
    if total_lines == 0:
        print("\033[33m[INFO] 'domains.txt' is empty.\033[0m")
        return

    working_count = 0
    dead_count = 0

    max_workers = 200  # Bumped to 200 threads for faster throughput on large lists
    print(f"\033[36mTesting {total_lines} configurations using {max_workers} concurrent threads...\033[0m\n")
    
    print('\033[?25l', end="")

    completed_count = 0
    lock = threading.Lock()
    
    working_buffer = []
    dead_buffer = set()
    logged_dead = set()

    # Initialize output files fresh at the start
    open(output_working, 'w', encoding='utf-8').close()
    open(output_dead, 'w', encoding='utf-8').close()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test_single_domain, line): line for line in lines}

        for future in as_completed(futures):
            line, is_alive, domain, is_skipped = future.result()
            
            with lock:
                completed_count += 1

                if is_skipped or is_alive:
                    working_count += 1
                    working_buffer.append(line)
                else:
                    dead_count += 1
                    d_lower = domain.lower()
                    if d_lower not in logged_dead:
                        logged_dead.add(d_lower)
                        dead_buffer.add(d_lower)

                if len(working_buffer) >= 500 or len(dead_buffer) >= 500:
                    if working_buffer:
                        with open(output_working, 'a', encoding='utf-8') as wf:
                            wf.writelines(working_buffer)
                        working_buffer.clear()
                    if dead_buffer:
                        with open(output_dead, 'a', encoding='utf-8') as df:
                            df.writelines([d + '\n' for d in dead_buffer])
                        dead_buffer.clear()

                percent = (completed_count / total_lines) * 100
                bar_length = 25
                filled_length = int(bar_length * completed_count // total_lines)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                
                status_str = f"\r\033[36m[{bar}]\033[0m \033[33m{percent:.1f}%\033[0m ({completed_count}/{total_lines}) | \033[32m{working_count} Working\033[0m | \033[31m{dead_count} Non Working\033[0m"
                print(status_str, end="", flush=True)

    if working_buffer:
        with open(output_working, 'a', encoding='utf-8') as wf:
            wf.writelines(working_buffer)
    if dead_buffer:
        with open(output_dead, 'a', encoding='utf-8') as df:
            df.writelines([d + '\n' for d in dead_buffer])

    print('\033[?25h', end="")
    print("\n")

    print(f"\033[32m[DONE]\033[0m Online configurations saved to \033[33m{output_working}\033[0m, dead domains saved to \033[33m{output_dead}\033[0m.")

if __name__ == '__main__':
    test_domains()
    input("\n\033[35mPress Enter to exit...\033[0m")