# Uptime Monitor

Check whether hosts are reachable (ping) and report status with latency.

## Requirements

- Python 3.8+
- Standard library only — no third-party packages
- The `ping` command (present on Linux and macOS)

## Usage

```bash
python3 main.py localhost
python3 main.py google.com 8.8.8.8
python3 main.py example.com --count 4 --timeout 3 --fail-on-down
```

## Example

```bash
$ python3 main.py localhost 8.8.8.8
HOST                           STATUS   LATENCY      DETAIL
----------------------------------------------------------------------
localhost                      UP       0.1 ms       2/2 replies
8.8.8.8                        UP       12.4 ms      2/2 replies

2/2 host(s) up.
```

## License

MIT — see [LICENSE](LICENSE).
