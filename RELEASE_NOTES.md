## ProxyTg v0.1.2

### English

Minimal console proxy manager for Telegram using Xray-core (VLESS + Reality).

**Download**

| File | Platform | Architecture |
|------|----------|--------------|
| `ProxyTg_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `ProxyTg_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `ProxyTg_win_amd64.zip` | Windows | x86-64 (amd64) |

**Quick start**

1. Download the archive for your OS
2. Extract it
3. Edit `client_config.json` — add your server details (or use `--vless "vless://..."`)
4. Run: `python3 teleproxy.py` (macOS/Linux) or `python teleproxy.py` (Windows)
5. In Telegram: Settings → Proxy → SOCKS5 → `127.0.0.1:2080`

**Components**

- ProxyTg 0.1.2
- Xray-core 26.2.6
- Python 3.7+

---

### Русский

Минимальный консольный прокси-менеджер для Telegram на базе Xray-core (VLESS + Reality).

**Скачивание**

| Файл | Платформа | Архитектура |
|------|-----------|-------------|
| `ProxyTg_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `ProxyTg_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `ProxyTg_win_amd64.zip` | Windows | x86-64 (amd64) |

**Быстрый старт**

1. Скачайте архив для вашей ОС
2. Распакуйте
3. Отредактируйте `client_config.json` — подставьте данные вашего сервера (или используйте `--vless "vless://..."`)
4. Запустите: `python3 teleproxy.py` (macOS/Linux) или `python teleproxy.py` (Windows)
5. В Telegram: Настройки → Прокси → SOCKS5 → `127.0.0.1:2080`

**Компоненты**

- ProxyTg 0.1.2
- Xray-core 26.2.6
- Python 3.7+
