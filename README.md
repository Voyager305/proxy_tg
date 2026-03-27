# proxy_manager_socks5_xray

**Local SOCKS5 proxy manager powered by Xray-core.**

Runs [Xray-core](https://github.com/XTLS/Xray-core) as a subprocess and exposes a local SOCKS5 port. Any application that supports SOCKS5 (browsers, messengers, CLI tools) can use it. No GUI, no root — just Python and one script.

Supports **VLESS + Reality** — a modern protocol resilient to blocking.

**[Russian version](README_RU.md)**

---

## Features

- Local SOCKS5 proxy for any application (browsers, Telegram, etc.)
- VLESS + Reality support (Xray-core 26+)
- Runs on **macOS**, **Linux**, and **Windows**
- One-command run, no installation
- Works with Telethon, Pyrogram, and any SOCKS5 client

## Download

Pick the archive for your OS:

| Platform | Archive | Architecture |
|----------|---------|--------------|
| macOS | `proxy_manager_socks5_xray_mac_arm64.zip` | ARM64 (Apple Silicon) |
| macOS | `proxy_manager_socks5_xray_mac_amd64.zip` | x86-64 (Intel) |
| Linux | `proxy_manager_socks5_xray_linux_amd64.zip` | x86-64 (amd64) |
| Windows | `proxy_manager_socks5_xray_win_amd64.zip` | x86-64 (amd64) |

Each archive is self-contained: script + Xray binary + geo data.

## Requirements

- **Python 3.7+**
- Xray-core is included in each package

## Quick start

### 1. Set up configuration

Edit `client_config.json` in your platform folder with your VLESS Reality server details:

| Field | Description |
|-------|-------------|
| `address` | Server IP or domain |
| `port` | Port (usually 443) |
| `id` | User UUID |
| `flow` | `xtls-rprx-vision` for Reality |
| `serverName` | SNI (e.g. `google.com`) |
| `password` | Reality public key |
| `shortId` | Short ID (hex, up to 16 chars) |

<details>
<summary><b>Filling from a VLESS link</b></summary>

If you have a link like `vless://uuid@host:port?...`, map the fields as follows:

```
vless://UUID@ADDRESS:PORT?type=tcp&security=reality&pbk=PASSWORD&fp=chrome&sni=SERVERNAME&sid=SHORTID&flow=xtls-rprx-vision#name
         │       │    │                                  │                       │            │
         ↓       ↓    ↓                                  ↓                       ↓            ↓
        id   address  port                            password              serverName      shortId
```

</details>

<details>
<summary><b>Example client_config.json</b></summary>

```json
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "port": 2080,
      "listen": "127.0.0.1",
      "protocol": "socks",
      "settings": { "auth": "noauth", "udp": true },
      "tag": "socks-in"
    }
  ],
  "outbounds": [
    {
      "protocol": "vless",
      "settings": {
        "vnext": [
          {
            "address": "YOUR_SERVER_IP_OR_DOMAIN",
            "port": 443,
            "users": [
              {
                "id": "YOUR-UUID-HERE",
                "encryption": "none",
                "flow": "xtls-rprx-vision"
              }
            ]
          }
        ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "fingerprint": "chrome",
          "serverName": "google.com",
          "password": "YOUR_PUBLIC_KEY_HERE",
          "shortId": "YOUR_SHORT_ID"
        }
      },
      "tag": "proxy"
    },
    {
      "protocol": "freedom",
      "tag": "direct"
    }
  ],
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "direct"
      }
    ]
  }
}
```

</details>

### 2. Run

Two options: VLESS link (easier) or JSON config.

**Option A — VLESS link (recommended):**

```bash
python3 teleproxy.py --vless "vless://UUID@HOST:PORT?type=tcp&security=reality&pbk=KEY&fp=chrome&sni=SNI&sid=SID&flow=xtls-rprx-vision#name"
```

Config is generated and saved. Next time just run:

```bash
python3 teleproxy.py
```

**Option B — manual JSON config:**

Fill in `client_config.json` (see example above) and run.

**macOS / Linux:**

```bash
cd proxy_manager_socks5_xray_mac_arm64    # or proxy_manager_socks5_xray_mac_amd64 / proxy_manager_socks5_xray_linux_amd64
python3 teleproxy.py
```

> On Linux you may need: `chmod +x xray-core/xray`

**Windows:**

```cmd
cd proxy_manager_socks5_xray_win_amd64
python teleproxy.py
```

The proxy will listen on **127.0.0.1:2080** (or the port set in config). Point any SOCKS5-capable app to this address.

## Using with other applications

The proxy is a standard **SOCKS5** server on `127.0.0.1:2080` (no auth). Use it with:

- **Browsers** — set system or browser proxy to SOCKS5, host `127.0.0.1`, port `2080`
- **curl / wget** — e.g. `curl --socks5 127.0.0.1:2080 https://example.com`
- **Any app** that supports SOCKS5 proxy (messengers, IDE, etc.)

To verify it works:

```bash
curl --socks5 127.0.0.1:2080 https://api.telegram.org
```

If you get JSON back, the proxy is up.

## Using with Telegram

To use it with Telegram:

**Telegram Desktop:**  
**Settings → Advanced → Proxy server settings → Add proxy**

| Parameter | Value |
|-----------|-------|
| Type | SOCKS5 |
| Host | `127.0.0.1` |
| Port | `2080` |

### Telethon / Pyrogram

Run the proxy in one terminal, your bot in another:

```python
# Telethon
from telethon import TelegramClient
import socks

client = TelegramClient(
    "session",
    api_id=YOUR_API_ID,
    api_hash="YOUR_API_HASH",
    proxy=(socks.SOCKS5, "127.0.0.1", 2080)
)
```

```python
# Pyrogram
from pyrogram import Client

app = Client(
    "session",
    api_id=YOUR_API_ID,
    api_hash="YOUR_API_HASH",
    proxy=dict(scheme="socks5", hostname="127.0.0.1", port=2080)
)
```

## Command-line options

```bash
python3 teleproxy.py                          # default config
python3 teleproxy.py -v "vless://..."    # from VLESS link (saves config)
python3 teleproxy.py -c my_config.json        # custom config file
python3 teleproxy.py -x /usr/local/bin/xray   # custom Xray path
python3 teleproxy.py -q                        # quiet (minimal output)
```

| Flag | Description |
|------|-------------|
| `-v`, `--vless` | VLESS URI — generates and saves config |
| `-c`, `--config` | Path to JSON config (default: `client_config.json`) |
| `-x`, `--xray` | Path to Xray binary |
| `-q`, `--quiet` | Minimal output |

## Project structure

```
proxy_manager_socks5_xray/
│
├── README.md
├── README_RU.md
├── LICENSE
│
├── proxy_manager_socks5_xray_mac_arm64/      # macOS (ARM64 / Apple Silicon)
│   ├── teleproxy.py
│   ├── client_config.json
│   ├── README.md
│   └── xray-core/
│       ├── xray
│       ├── LICENSE-Xray.txt   # MPL 2.0
│       ├── geoip.dat
│       └── geosite.dat
│
├── proxy_manager_socks5_xray_mac_amd64/      # macOS (x86-64 / Intel)
│   ├── teleproxy.py
│   ├── client_config.json
│   ├── README.md
│   └── xray-core/
│       ├── xray
│       ├── LICENSE-Xray.txt   # MPL 2.0
│       ├── geoip.dat
│       └── geosite.dat
│
├── proxy_manager_socks5_xray_linux_amd64/    # Linux (x86-64 / amd64)
│   ├── teleproxy.py
│   ├── client_config.json
│   ├── README.md
│   └── xray-core/
│       ├── xray
│       ├── LICENSE-Xray.txt   # MPL 2.0
│       ├── geoip.dat
│       └── geosite.dat
│
└── proxy_manager_socks5_xray_win_amd64/      # Windows (x86-64 / amd64)
    ├── teleproxy.py
    ├── client_config.json
    ├── README.md
    └── xray-core/
        ├── xray.exe
        ├── LICENSE-Xray.txt   # MPL 2.0
        ├── wintun.dll
        ├── geoip.dat
        └── geosite.dat
```

## FAQ

**Q: macOS says "The file 'xray' could not be opened", Apple can't verify the developer. What do I do?**  
The Xray binary is not signed by Apple (normal for open-source). To allow it:
- **Option 1:** Click "Done", then open **System Settings → Privacy & Security** — at the bottom you'll see "Open Anyway" for this app.
- **Option 2:** In a terminal, from the project folder run:
  ```bash
  xattr -d com.apple.quarantine xray-core/xray
  ```
  Then `python3 teleproxy.py` will run xray without the warning.

**Q: Port 2080 is already in use. How do I change it?**  
Change `"port": 2080` in `client_config.json` to any free port (e.g. 1080, 9050).

**Q: Do I need my own server?**  
Yes. You need a VPS with an Xray server (VLESS + Reality). That's the server side; proxy_manager_socks5_xray is the client only.

**Q: How do I update Xray-core?**  
Download a new binary from [releases](https://github.com/XTLS/Xray-core/releases) and replace the file in the `xray-core/` folder.

## Component versions

| Component | Version |
|-----------|--------|
| proxy_manager_socks5_xray | 0.1.3 |
| Xray-core | 26.2.6 |

## Notes

- In Xray 26+ the Reality public key field is named `password` (not `publicKey`)
- For debugging, set `"loglevel"` to `"debug"` in the config
- The script does not require admin/root
- Each platform folder is self-contained and can be distributed on its own

## Third-party license

The **Xray-core** binary in each `xray-core/` folder is distributed under the **Mozilla Public License 2.0 (MPL 2.0)**. The full license text is in `xray-core/LICENSE-Xray.txt`. Source: [XTLS/Xray-core](https://github.com/XTLS/Xray-core).

## License

[MIT](LICENSE)
