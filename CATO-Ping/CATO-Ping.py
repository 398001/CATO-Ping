#!/usr/bin/env python3
"""
CATO-Ping — continuous TCP ping with latency, ASN lookup and colored console output.

Usage:
    python catoping.py <host> [-p PORT] [-i INTERVAL] [-t TIMEOUT] [--no-lookup] [--label NAME]
"""

import argparse
import os
import socket
import subprocess
import sys
import time
from datetime import datetime


class Color:
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    RED     = "\033[91m"
    GRAY    = "\033[90m"
    WHITE   = "\033[97m"
    RESET   = "\033[0m"


TAG = "[CATO-Ping]"


def enable_ansi() -> None:
    if os.name == "nt":
        os.system("")


def resolve_host(host: str) -> str:
    return socket.gethostbyname(host)


def tcp_ping(ip: str, port: int, timeout: float) -> float | None:
    """Returns connection time in ms, or None on timeout/failure."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            start = time.perf_counter()
            s.connect((ip, port))
            return (time.perf_counter() - start) * 1000
    except OSError:
        return None


def lookup_asn(ip: str) -> str | None:
    """Resolves ASN + organization name via Team Cymru DNS."""
    try:
        rev = ".".join(reversed(ip.split(".")))
        out = subprocess.run(
            ["nslookup", "-type=TXT", f"{rev}.origin.asn.cymru.com"],
            capture_output=True, text=True, timeout=4,
        ).stdout
        for line in out.splitlines():
            if "text =" in line.lower() and '"' in line:
                asn = line.split('"')[1].split("|")[0].strip()
                out2 = subprocess.run(
                    ["nslookup", "-type=TXT", f"AS{asn}.asn.cymru.com"],
                    capture_output=True, text=True, timeout=4,
                ).stdout
                for l in out2.splitlines():
                    if "text =" in l.lower() and '"' in l:
                        org = l.split('"')[1].split("|")[-1].strip()
                        return f"AS{asn} {org}"
    except Exception:
        pass
    return None


def lookup_rdns(ip: str) -> str | None:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def build_label(host: str, ip: str, no_lookup: bool, custom: str | None) -> str:
    if custom:
        return custom
    if no_lookup:
        return ip
    if host.replace(".", "").isdigit():
        return lookup_asn(ip) or lookup_rdns(ip) or ip
    return host


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="CATO-Ping",
        description="Continuous TCP ping with latency, ASN lookup and colored output.",
    )
    p.add_argument("host", help="target IP or domain")
    p.add_argument("-p", "--port", type=int, default=80, help="TCP port (default: 80)")
    p.add_argument("-i", "--interval", type=float, default=1.0, help="seconds between pings (default: 1.0)")
    p.add_argument("-t", "--timeout", type=float, default=2.0, help="timeout in seconds (default: 2.0)")
    p.add_argument("--no-lookup", action="store_true", help="skip ASN/rDNS lookup")
    p.add_argument("--label", help="custom display name")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    enable_ansi()

    try:
        ip = resolve_host(args.host)
    except socket.gaierror:
        print(f"{Color.RED}[-] Could not resolve host: {args.host}{Color.RESET}")
        sys.exit(1)

    label = build_label(args.host, ip, args.no_lookup, args.label)

    print(
        f"{Color.CYAN}[*] Target : {ip}:{args.port}{Color.RESET}\n"
        f"{Color.CYAN}[*] Network: {label}{Color.RESET}\n"
        f"{Color.GRAY}[*] Stopping with Ctrl+C{Color.RESET}\n",
        flush=True,
    )

    sent = ok = 0
    total = 0.0
    min_ms = max_ms = None

    try:
        while True:
            loop_start = time.perf_counter()
            sent += 1

            ts = datetime.now().strftime("%H:%M:%S.%f")[:-4]
            ms = tcp_ping(ip, args.port, args.timeout)

            if ms is not None:
                ok += 1
                total += ms
                min_ms = ms if min_ms is None else min(min_ms, ms)
                max_ms = ms if max_ms is None else max(max_ms, ms)
                print(
                    f"{Color.MAGENTA}{TAG}{Color.RESET} "
                    f"{Color.GREEN}{ts}{Color.RESET} "
                    f"{Color.GRAY}({Color.CYAN}{label}{Color.RESET}{Color.GRAY}){Color.RESET}: "
                    f"{Color.WHITE}{ms:6.2f}ms{Color.RESET} "
                    f"{Color.GRAY}protocol=TCP port={args.port}{Color.RESET}"
                )
            else:
                print(
                    f"{Color.MAGENTA}{TAG}{Color.RESET} "
                    f"{Color.GREEN}{ts}{Color.RESET} "
                    f"{Color.RED}timed out ({label}){Color.RESET}: "
                    f"{Color.GRAY}protocol=TCP port={args.port}{Color.RESET}"
                )

            # exact interval: sleep only the remaining time
            elapsed = time.perf_counter() - loop_start
            time.sleep(max(0.0, args.interval - elapsed))

    except KeyboardInterrupt:
        pass

    lost = sent - ok
    loss = 100.0 * lost / sent if sent else 0.0
    avg = total / ok if ok else 0.0

    print(f"\n{Color.GRAY}{'─' * 29}{Color.RESET}")
    print(f"{Color.GRAY}Sent      : {sent}")
    print(f"Received  : {Color.GREEN}{ok}{Color.GRAY}")
    print(f"Lost      : {Color.RED}{lost}{Color.GRAY} ({loss:.1f}%)")
    if ok:
        print(f"Latency   : avg {avg:.2f} ms | min {min_ms:.2f} ms | max {max_ms:.2f} ms")
    print(Color.RESET, end="")


if __name__ == "__main__":
    main()