## proxy_manager_socks5_xray v0.1.2

### English

Local SOCKS5 proxy manager powered by Xray-core (VLESS + Reality). Use with any SOCKS5-capable app; originally made for Telegram.

**What's new**

- Application renamed to **proxy_manager_socks5_xray** (from ProxyTg)
- Positioned as a universal SOCKS5 proxy for any application; Telegram is documented as one of the use cases
- Platform folders and release archives no longer include version in names (e.g. `proxy_manager_socks5_xray_mac_arm64.zip`)
- Xray-core binaries and geo data are now included in the repository (previously ignored by git)

**Fixed / improved**

- Documentation restructured: separate section “Using with Telegram”, new section “Using with other applications” (browsers, curl, any SOCKS5 app)
- Telegram Desktop path updated: **Settings → Advanced → Proxy server settings → Add proxy**
- Script startup message shows SOCKS5 address first, then Telegram as a hint

**Download**

| File | Platform | Architecture |
|------|----------|--------------|
| `proxy_manager_socks5_xray_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `proxy_manager_socks5_xray_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `proxy_manager_socks5_xray_win_amd64.zip` | Windows | x86-64 (amd64) |

**Quick start**

1. Download the archive for your OS
2. Extract it
3. Edit `client_config.json` — add your server details (or use `--vless "vless://..."`)
4. Run: `python3 teleproxy.py` (macOS/Linux) or `python teleproxy.py` (Windows)
5. Point any app to SOCKS5 `127.0.0.1:2080`. For Telegram: Settings → Advanced → Proxy server settings → Add proxy.

**Components**

- proxy_manager_socks5_xray 0.1.2
- Xray-core 26.2.6
- Python 3.7+

---

### Русский

Локальный SOCKS5 прокси-менеджер на базе Xray-core (VLESS + Reality). Подходит для любого приложения с поддержкой SOCKS5; изначально делался под Telegram.

**Что нового**

- Приложение переименовано в **proxy_manager_socks5_xray** (ранее ProxyTg)
- Позиционируется как универсальный SOCKS5 прокси для любого приложения; Telegram описан как один из сценариев
- В названиях папок и архивов релиза убрана версионность (например, `proxy_manager_socks5_xray_mac_arm64.zip`)
- Ядра Xray и geo-файлы теперь включены в репозиторий (ранее были в .gitignore)

**Исправления и изменения**

- Документация переструктурирована: отдельный блок «Использование с Telegram», новый блок «Использование с другими приложениями» (браузеры, curl, любое приложение с SOCKS5)
- Обновлён путь в Telegram Desktop: **Настройки → Продвинутые настройки → Настройки прокси сервера → Добавить прокси**
- При запуске скрипта сначала выводится адрес SOCKS5, затем подсказка по Telegram

**Скачивание**

| Файл | Платформа | Архитектура |
|------|-----------|-------------|
| `proxy_manager_socks5_xray_mac_arm64.zip` | macOS | ARM64 (Apple Silicon) |
| `proxy_manager_socks5_xray_linux_amd64.zip` | Linux | x86-64 (amd64) |
| `proxy_manager_socks5_xray_win_amd64.zip` | Windows | x86-64 (amd64) |

**Быстрый старт**

1. Скачайте архив для вашей ОС
2. Распакуйте
3. Отредактируйте `client_config.json` — подставьте данные вашего сервера (или используйте `--vless "vless://..."`)
4. Запустите: `python3 teleproxy.py` (macOS/Linux) или `python teleproxy.py` (Windows)
5. Укажите в любом приложении SOCKS5 `127.0.0.1:2080`. Для Telegram: Настройки → Продвинутые настройки → Настройки прокси сервера → Добавить прокси.

**Компоненты**

- proxy_manager_socks5_xray 0.1.2
- Xray-core 26.2.6
- Python 3.7+
