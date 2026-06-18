#!/usr/bin/env python3
"""
ngrok runner script to expose local project to the internet
"""

import subprocess
import time
import sys
import shutil
import urllib.request
import urllib.error
import json

def run_ngrok(local_port=8501, ngrok_config=None):
    """
    Start ngrok tunnel for local port
    
    Args:
        local_port (int): Local port to expose (default: 8000)
        ngrok_config (str): Optional path to ngrok config file
    """
    process = None
    try:
        # Ensure ngrok is installed / available
        ngrok_exe = shutil.which("ngrok")
        if not ngrok_exe:
            print("Error: ngrok not found in PATH. Please install ngrok:")
            print("https://ngrok.com/download")
            sys.exit(1)

        # Build ngrok command
        cmd = [ngrok_exe, "http", str(local_port), "--log=stdout"]
        if ngrok_config:
            cmd.extend(["--config", ngrok_config])

        print(f"Starting ngrok tunnel on port {local_port}...")
        print(f"Command: {' '.join(cmd)}")

        # Start ngrok process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Poll local ngrok API for public URL
        api_url = "http://127.0.0.1:4040/api/tunnels"
        public_url = None
        start = time.time()
        timeout = 30
        while time.time() - start < timeout:
            try:
                with urllib.request.urlopen(api_url, timeout=3) as resp:
                    data = resp.read().decode("utf-8")
                    info = json.loads(data)
                    tunnels = info.get("tunnels", [])
                    if tunnels:
                        # Prefer https tunnel
                        for t in tunnels:
                            if t.get("proto") == "https":
                                public_url = t.get("public_url")
                                break
                        if not public_url:
                            public_url = tunnels[0].get("public_url")
                        break
            except urllib.error.URLError:
                pass
            except Exception:
                pass

            # Check if process terminated unexpectedly
            if process and process.poll() is not None:
                print("ngrok process exited unexpectedly.")
                # print a bit of output for debugging
                try:
                    if process.stdout:
                        out = process.stdout.read().decode(errors="ignore")
                    else:
                        out = ""
                    print(out[:1000])
                except Exception:
                    pass
                sys.exit(1)

            time.sleep(0.5)

        if public_url:
            print(f"ngrok tunnel established: {public_url}")
            print("Forwarding local port", local_port)
            try:
                # Keep process running until user interrupts
                process.wait()
            except KeyboardInterrupt:
                print("\nShutting down ngrok...")
                process.terminate()
                process.wait()
        else:
            print("Failed to determine ngrok public URL within timeout.")
            print("If ngrok started, check the web UI at C")
            try:
                if process:
                    process.terminate()
            except Exception:
                pass
            sys.exit(1)
        
    except FileNotFoundError:
        print("Error: ngrok not found. Please install ngrok first.")
        print("Download from: https://ngrok.com/download")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down ngrok...")
        if process:
            try:
                process.terminate()
                process.wait()
            except Exception:
                pass
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)
    
    run_ngrok(local_port=port)
