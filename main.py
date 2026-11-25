#!/usr/bin/env python3
"""Check whether hosts are reachable (ping) and report status."""
import argparse
import re
import subprocess
import sys

LATENCY_RE = re.compile(r"time[=<]([\d.]+)\s*ms")


def ping_host(host, count, timeout):
    """Return (up, latency_ms_or_None, detail)."""
    cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * count + 5)
    except FileNotFoundError:
        return None, None, "ping command not found"
    except subprocess.TimeoutExpired:
        return False, None, "timed out"
    text = out.stdout + out.stderr
    latencies = [float(m) for m in LATENCY_RE.findall(text)]
    avg = sum(latencies) / len(latencies) if latencies else None
    if out.returncode == 0:
        return True, avg, f"{len(latencies)}/{count} replies"
    return False, avg, "no reply"


def main():
    p = argparse.ArgumentParser(description="Check whether hosts are reachable (ping) and report status.")
    p.add_argument("hosts", nargs="+", help="Hostnames or IPs to check")
    p.add_argument("--count", type=int, default=2, help="Pings per host (default: 2)")
    p.add_argument("--timeout", type=int, default=2, help="Seconds to wait per ping (default: 2)")
    p.add_argument("--fail-on-down", action="store_true",
                   help="Exit non-zero if any host is down")
    args = p.parse_args()
    if args.count < 1:
        p.error("--count must be at least 1")

    results = []
    for host in args.hosts:
        up, latency, detail = ping_host(host, args.count, args.timeout)
        results.append((host, up, latency, detail))

    print(f"{'HOST':<30} {'STATUS':<8} {'LATENCY':<12} DETAIL")
    print("-" * 70)
    for host, up, latency, detail in results:
        status = "UP" if up else ("UNKNOWN" if up is None else "DOWN")
        lat = f"{latency:.1f} ms" if latency is not None else "-"
        print(f"{host:<30} {status:<8} {lat:<12} {detail}")
    up_count = sum(1 for _h, u, _l, _d in results if u)
    print(f"\n{up_count}/{len(results)} host(s) up.")
    if args.fail_on_down and up_count < len(results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
