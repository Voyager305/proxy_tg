## proxy_manager_socks5_xray v0.1.3

### English

Local SOCKS5 proxy manager powered by Xray-core (VLESS + Reality). Use with any SOCKS5-capable app.

**What's new**

- Added a separate **Intel Mac** package: `proxy_manager_socks5_xray_mac_amd64.zip`
- Main documentation updated to include Intel macOS in download and run sections

**Download**

| File | Platform | Architecture |
|------|----------|--------------|
| `proxy_manager_socks5_xray_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `proxy_manager_socks5_xray_mac_amd64.zip` | macOS | x86-64 (Intel) |
| `proxy_manager_socks5_xray_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `proxy_manager_socks5_xray_win_amd64.zip` | Windows | x86-64 (amd64) |

**Quick start**

1. Download the archive for your OS
2. Extract it
3. Edit `client_config.json` — add your server details (or use `--vless "vless://..."`)
4. Run: `python3 teleproxy.py` (macOS/Linux) or `python teleproxy.py` (Windows)
5. Point any app to SOCKS5 `127.0.0.1:2080`. For Telegram: Settings → Advanced → Proxy server settings → Add proxy.

**Components**

- proxy_manager_socks5_xray 0.1.3
- Xray-core 26.2.6
- Python 3.7+

---

### Русский

Локальный SOCKS5 прокси-менеджер на базе Xray-core (VLESS + Reality). Подходит для любого приложения с поддержкой SOCKS5.

**Что нового**

- Добавлен отдельный пакет для **Intel Mac**: `proxy_manager_socks5_xray_mac_amd64.zip`
- Основная документация обновлена: добавлена Intel-версия macOS в разделы скачивания и запуска

**Скачивание**

| Файл | Платформа | Архитектура |
|------|-----------|-------------|
| `proxy_manager_socks5_xray_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `proxy_manager_socks5_xray_mac_amd64.zip` | macOS | x86-64 (Intel) |
| `proxy_manager_socks5_xray_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `proxy_manager_socks5_xray_win_amd64.zip` | Windows | x86-64 (amd64) |

**Быстрый старт**

1. Скачайте архив для вашей ОС
2. Распакуйте
3. Отредактируйте `client_config.json` — подставьте данные вашего сервера (или используйте флаг при запуске `--vless "vless://..."`)
4. Запустите: `python3 teleproxy.py` (macOS/Linux) или `python teleproxy.py` (Windows)
5. Укажите в любом приложении SOCKS5 `127.0.0.1:2080`. Для Telegram: Настройки → Продвинутые настройки → Настройки прокси сервера → Добавить прокси.

**Компоненты**

- proxy_manager_socks5_xray 0.1.3
- Xray-core 26.2.6
- Python 3.7+
