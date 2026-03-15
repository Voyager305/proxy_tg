## ProxyTg v0.1.1

Минимальный консольный прокси-менеджер для Telegram на базе Xray-core (VLESS + Reality).

### Скачивание

| Файл | Платформа | Архитектура |
|------|-----------|-------------|
| `ProxyTg_v0.1.1_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `ProxyTg_v0.1.1_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `ProxyTg_v0.1.1_win_amd64.zip` | Windows | x86-64 (amd64) |

### Быстрый старт

1. Скачайте архив для вашей ОС
2. Распакуйте
3. Отредактируйте `client_config.json` — подставьте данные вашего сервера
4. Запустите: `python3 teleproxy.py` (macOS/Linux) или `python teleproxy.py` (Windows)
5. В Telegram: Settings → Proxy → SOCKS5 → `127.0.0.1:2080`

### Компоненты

- ProxyTg 0.1.1
- Xray-core 26.2.6
- Python 3.7+
