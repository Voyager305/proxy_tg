# ProxyTg

Минимальный консольный прокси-менеджер для Telegram. Запускает Xray-core как subprocess и поднимает локальный SOCKS5 порт — без GUI, без лишних зависимостей.

## Требования

- Python 3.7+
- Xray-core (уже включён в проект)

## Быстрый старт

1. **Настройте конфигурацию** — отредактируйте `client_config.json`, подставьте данные от вашего VLESS Reality сервера:

| Поле | Описание |
|------|----------|
| `address` | Адрес сервера (домен или IP) |
| `port` | Порт (обычно 443) |
| `id` | UUID пользователя |
| `flow` | `xtls-rprx-vision` для Reality |
| `serverName` | SNI (например, www.google.com) |
| `password` | Публичный ключ Reality (из `xray x25519 -i "приватный_ключ_сервера"`) |
| `shortId` | Short ID (16 hex-символов или меньше) |

   Пример `client_config.json`:

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
            "address": "YOUR_SERVER_ADDRESS",   ← IP или домен сервера
            "port": 443,                        ← порт сервера
            "users": [
              {
                "id": "YOUR_UUID",              ← UUID пользователя
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
          "serverName": "google.com",           ← SNI (должен совпадать с сервером)
          "password": "YOUR_PUBLIC_KEY",        ← публичный ключ Reality
          "shortId": "YOUR_SHORT_ID"            ← Short ID
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

   Если у вас есть VLESS-ссылка вида `vless://uuid@host:port?...`, поля заполняются так:

```
vless://UUID@ADDRESS:PORT?type=tcp&security=reality&pbk=PASSWORD&fp=chrome&sni=SERVERNAME&sid=SHORTID&flow=xtls-rprx-vision#название
         │       │    │                                  │                       │            │
         ↓       ↓    ↓                                  ↓                       ↓            ↓
        id   address  port                            password              serverName      shortId
```

2. **Запустите** (один из способов):
   ```cmd
   :: Способ A — из VLESS-ссылки (проще, конфиг сохранится автоматически):
   python teleproxy.py --vless "vless://UUID@HOST:PORT?type=tcp&security=reality&pbk=KEY&fp=chrome&sni=SNI&sid=SID&flow=xtls-rprx-vision#name"

   :: Способ B — из JSON-конфига (заполните client_config.json вручную):
   python teleproxy.py
   ```

3. **Настройте Telegram:** Settings → Data and Storage → Proxy → SOCKS5 → Host: `127.0.0.1`, Port: `2080`

## Опции запуска

```cmd
python teleproxy.py --vless "vless://..."    :: из VLESS-ссылки
python teleproxy.py -c client_config.json    :: другой конфиг
python teleproxy.py -x C:\path\to\xray.exe   :: путь к бинарнику
python teleproxy.py -q                       :: тихий режим
```

## Использование с Telethon

```python
from telethon import TelegramClient
from telethon.sessions import StringSession
import socks

client = TelegramClient(
    StringSession(),
    api_id=YOUR_API_ID,
    api_hash=YOUR_API_HASH,
    proxy=(socks.SOCKS5, '127.0.0.1', 2080)
)
```

Запустите `teleproxy.py` в одном терминале, ваш бот — в другом.

## Структура проекта

```
teleproxy\
├── teleproxy.py        # основной скрипт
├── client_config.json  # конфигурация (заполните своими данными)
├── README.md
└── xray-core\          # компоненты Xray
    ├── xray.exe        # бинарник (Windows amd64)
    ├── wintun.dll      # драйвер TUN для Windows
    ├── geoip.dat       # база GeoIP для маршрутизации
    └── geosite.dat     # база GeoSite для маршрутизации
```

## Примечания

- В Xray 26+ поле публичного ключа Reality называется `password` (не `publicKey`)
- Для отладки измените `loglevel` в конфиге на `debug`
- Убедитесь, что Python добавлен в PATH при установке (галочка "Add Python to PATH" в инсталляторе)
