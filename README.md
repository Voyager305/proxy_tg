# ProxyTg v0.1.1

**Минимальный консольный прокси-менеджер для Telegram.**

Запускает [Xray-core](https://github.com/XTLS/Xray-core) как subprocess и поднимает локальный SOCKS5 порт. Без GUI, без root, без лишних зависимостей — только Python и один скрипт.

Поддерживает протокол **VLESS + Reality** — современный и устойчивый к блокировкам.

---

## Возможности

- Локальный SOCKS5 прокси для Telegram (десктоп и мобильный)
- Поддержка VLESS + Reality (Xray-core 26+)
- Работает на **macOS**, **Linux** и **Windows**
- Запуск одной командой, без установки
- Совместимость с Telethon, Pyrogram и любыми SOCKS5-клиентами

## Скачивание

Выберите архив для вашей ОС:

| Платформа | Архив | Архитектура |
|-----------|-------|-------------|
| macOS | `ProxyTg_v0.1.1_mac_arm64.zip` | ARM64 (Apple Silicon) |
| Linux | `ProxyTg_v0.1.1_linux_amd64.zip` | x86-64 (amd64) |
| Windows | `ProxyTg_v0.1.1_win_amd64.zip` | x86-64 (amd64) |

Каждая папка — самодостаточный пакет: скрипт + бинарник Xray + geo-файлы.

## Требования

- **Python 3.7+**
- Xray-core — уже включён в каждый пакет

## Быстрый старт

### 1. Заполните конфигурацию

Отредактируйте `client_config.json` в папке для вашей ОС, подставив данные от вашего VLESS Reality сервера:

| Поле | Описание |
|------|----------|
| `address` | IP-адрес или домен сервера |
| `port` | Порт (обычно 443) |
| `id` | UUID пользователя |
| `flow` | `xtls-rprx-vision` для Reality |
| `serverName` | SNI (например, `google.com`) |
| `password` | Публичный ключ Reality |
| `shortId` | Short ID (hex, до 16 символов) |

<details>
<summary><b>Как заполнить из VLESS-ссылки</b></summary>

Если у вас есть ссылка вида `vless://uuid@host:port?...`, поля заполняются так:

```
vless://UUID@ADDRESS:PORT?type=tcp&security=reality&pbk=PASSWORD&fp=chrome&sni=SERVERNAME&sid=SHORTID&flow=xtls-rprx-vision#название
         │       │    │                                  │                       │            │
         ↓       ↓    ↓                                  ↓                       ↓            ↓
        id   address  port                            password              serverName      shortId
```

</details>

<details>
<summary><b>Пример client_config.json</b></summary>

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

### 2. Запустите

Есть два способа — через VLESS-ссылку (проще) или через JSON-конфиг:

**Способ A — VLESS-ссылка (рекомендуется):**

```bash
python3 teleproxy.py --vless "vless://UUID@HOST:PORT?type=tcp&security=reality&pbk=KEY&fp=chrome&sni=SNI&sid=SID&flow=xtls-rprx-vision#name"
```

Конфиг сгенерируется и сохранится автоматически. При следующем запуске достаточно:

```bash
python3 teleproxy.py
```

**Способ B — ручной JSON-конфиг:**

Заполните `client_config.json` (см. пример выше) и запустите.

**macOS / Linux:**

```bash
cd proxy_tg_mac_v0.1.1    # или proxy_tg_linux_v0.1.1
python3 teleproxy.py
```

> На Linux может потребоваться: `chmod +x xray-core/xray`

**Windows:**

```cmd
cd proxy_tg_win_v0.1.1
python teleproxy.py
```

### 3. Настройте Telegram

Откройте Telegram Desktop:

**Settings → Data and Storage → Proxy → Add Proxy**

| Параметр | Значение |
|----------|----------|
| Type | SOCKS5 |
| Host | `127.0.0.1` |
| Port | `2080` |

Telegram Mobile: Settings → Data and Storage → Proxy → SOCKS5 → те же параметры.

## Опции запуска

```bash
python3 teleproxy.py                          # запуск с настройками по умолчанию
python3 teleproxy.py --vless "vless://..."    # запуск из VLESS-ссылки (сохраняет конфиг)
python3 teleproxy.py -c my_config.json        # другой конфиг
python3 teleproxy.py -x /usr/local/bin/xray   # свой путь к Xray
python3 teleproxy.py -q                       # тихий режим (без логов)
```

| Флаг | Описание |
|------|----------|
| `-v`, `--vless` | VLESS URI — автоматически генерирует и сохраняет конфиг |
| `-c`, `--config` | Путь к JSON-конфигу (по умолчанию `client_config.json`) |
| `-x`, `--xray` | Путь к бинарнику Xray |
| `-q`, `--quiet` | Минимальный вывод |

## Использование с Telethon / Pyrogram

Запустите ProxyTg в одном терминале, бот — в другом:

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

## Структура проекта

```
proxy_tg_v0.1.1/
│
├── README.md                        # этот файл
├── LICENSE
│
├── proxy_tg_mac_v0.1.1/            # macOS (ARM64 / Apple Silicon)
│   ├── teleproxy.py
│   ├── client_config.json
│   ├── README.md
│   └── xray-core/
│       ├── xray
│       ├── geoip.dat
│       └── geosite.dat
│
├── proxy_tg_linux_v0.1.1/          # Linux (x86-64 / amd64)
│   ├── teleproxy.py
│   ├── client_config.json
│   ├── README.md
│   └── xray-core/
│       ├── xray
│       ├── geoip.dat
│       └── geosite.dat
│
└── proxy_tg_win_v0.1.1/            # Windows (x86-64 / amd64)
    ├── teleproxy.py
    ├── client_config.json
    ├── README.md
    └── xray-core/
        ├── xray.exe
        ├── wintun.dll
        ├── geoip.dat
        └── geosite.dat
```

## FAQ

**Q: Порт 2080 уже занят, как сменить?**
Измените `"port": 2080` в `client_config.json` на любой свободный (например, 1080, 9050).

**Q: Как проверить, что прокси работает?**
```bash
curl --socks5 127.0.0.1:2080 https://api.telegram.org
```
Если возвращает JSON — прокси работает.

**Q: Нужен ли свой сервер?**
Да, вам нужен VPS с настроенным Xray-сервером (VLESS + Reality). Это серверная часть, ProxyTg — только клиент.

**Q: Как обновить Xray-core?**
Скачайте новый бинарник с [releases](https://github.com/XTLS/Xray-core/releases) и замените файл в папке `xray-core/`.

## Версии компонентов

| Компонент | Версия |
|-----------|--------|
| ProxyTg | 0.1.1 |
| Xray-core | 26.2.6 |

## Примечания

- В Xray 26+ поле публичного ключа Reality называется `password` (не `publicKey`)
- Для отладки измените `"loglevel"` в конфиге на `"debug"`
- Скрипт не требует прав администратора / root
- Каждая платформенная папка полностью автономна — можно распространять отдельно

## Лицензия

[MIT](LICENSE)
