#!/usr/bin/env python3
"""
ProxyTg — минимальный консольный менеджер прокси для Telegram.
Запускает Xray-core как subprocess и держит локальный SOCKS5 порт.
"""

import subprocess
import sys
import os
import signal
import time
import json
import argparse
from urllib.parse import urlparse, parse_qs, unquote

# Конфигурация по умолчанию
XRAY_BINARY = r".\xray-core\xray.exe"
CONFIG_FILE = "client_config.json"
LOCAL_SOCKS_PORT = 2080


def find_xray() -> str:
    """Ищет бинарник xray: рядом со скриптом, в PATH или в текущей директории."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "xray-core", "xray.exe"),
        os.path.join(script_dir, "xray.exe"),
        "xray.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
        if path == "xray.exe":
            try:
                result = subprocess.run(
                    ["where", "xray.exe"], capture_output=True
                )
                if result.returncode == 0:
                    return path
            except FileNotFoundError:
                pass
    return XRAY_BINARY


def parse_vless_uri(uri: str) -> dict:
    """Парсит VLESS URI вида vless://UUID@HOST:PORT?params#name."""
    if not uri.startswith("vless://"):
        print("Ошибка: ссылка должна начинаться с vless://")
        sys.exit(1)
    parsed = urlparse(uri)
    if not parsed.hostname or not parsed.port or not parsed.username:
        print("Ошибка: неверный формат VLESS URI")
        print("Формат: vless://UUID@HOST:PORT?type=tcp&security=reality&pbk=KEY&sni=SNI&sid=SID&flow=FLOW")
        sys.exit(1)
    params = parse_qs(parsed.query)
    return {
        "id": unquote(parsed.username),
        "address": parsed.hostname,
        "port": parsed.port,
        "flow": params.get("flow", [""])[0],
        "security": params.get("security", [""])[0],
        "sni": params.get("sni", [""])[0],
        "pbk": params.get("pbk", [""])[0],
        "sid": params.get("sid", [""])[0],
        "fp": params.get("fp", ["chrome"])[0],
        "network": params.get("type", ["tcp"])[0],
    }


def generate_config(vless: dict, socks_port: int = 2080) -> dict:
    """Генерирует Xray-конфиг из распарсенного VLESS URI."""
    config = {
        "log": {"loglevel": "warning"},
        "inbounds": [{
            "port": socks_port,
            "listen": "127.0.0.1",
            "protocol": "socks",
            "settings": {"auth": "noauth", "udp": True},
            "tag": "socks-in",
        }],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [{
                        "address": vless["address"],
                        "port": vless["port"],
                        "users": [{
                            "id": vless["id"],
                            "encryption": "none",
                            "flow": vless["flow"],
                        }],
                    }],
                },
                "streamSettings": {
                    "network": vless["network"],
                    "security": vless["security"],
                    "realitySettings": {
                        "fingerprint": vless["fp"],
                        "serverName": vless["sni"],
                        "password": vless["pbk"],
                        "shortId": vless["sid"],
                    },
                },
                "tag": "proxy",
            },
            {"protocol": "freedom", "tag": "direct"},
        ],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [{"type": "field", "ip": ["geoip:private"], "outboundTag": "direct"}],
        },
    }
    return config


def load_config(config_path: str) -> dict:
    """Загружает и валидирует JSON-конфиг."""
    if not os.path.isfile(config_path):
        print(f"Ошибка: файл конфигурации не найден: {config_path}")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Ошибка в JSON конфигурации: {e}")
            sys.exit(1)


def validate_config(config: dict) -> bool:
    """Проверяет наличие обязательных полей."""
    if "inbounds" not in config or not config["inbounds"]:
        print("Ошибка: в конфиге должен быть хотя бы один inbound")
        return False
    if "outbounds" not in config or not config["outbounds"]:
        print("Ошибка: в конфиге должен быть хотя бы один outbound")
        return False
    return True


def get_socks_port(config: dict) -> int:
    """Извлекает порт SOCKS из конфига."""
    for ib in config.get("inbounds", []):
        if ib.get("protocol") == "socks":
            return ib.get("port", LOCAL_SOCKS_PORT)
    return LOCAL_SOCKS_PORT


def main():
    parser = argparse.ArgumentParser(
        description="ProxyTg — локальный SOCKS5 прокси через Xray (VLESS/Reality)"
    )
    parser.add_argument(
        "-c", "--config",
        default=CONFIG_FILE,
        help=f"Путь к конфигу (по умолчанию: {CONFIG_FILE})",
    )
    parser.add_argument(
        "-x", "--xray",
        default=None,
        help="Путь к бинарнику Xray (по умолчанию: .\\xray-core\\xray.exe или в PATH)",
    )
    parser.add_argument(
        "-v", "--vless",
        default=None,
        help='VLESS URI (vless://UUID@HOST:PORT?...)',
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Минимальный вывод в консоль",
    )
    args = parser.parse_args()

    xray_path = args.xray or find_xray()
    config_path = os.path.abspath(args.config)

    if not os.path.isfile(xray_path):
        print(f"Ошибка: Xray не найден: {xray_path}")
        print("Скачайте с https://github.com/XTLS/Xray-core/releases")
        print("Для Windows: Xray-windows-64.zip (amd64) или Xray-windows-arm64-v8a.zip")
        sys.exit(1)

    if args.vless:
        vless = parse_vless_uri(args.vless)
        config = generate_config(vless)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        if not args.quiet:
            print(f"Конфиг из VLESS URI сохранён: {config_path}")
    else:
        config = load_config(config_path)

    if not validate_config(config):
        sys.exit(1)

    socks_port = get_socks_port(config)

    if not args.quiet:
        print("=" * 50)
        print("  ProxyTg — прокси для Telegram")
        print("=" * 50)
        print(f"  Xray:     {xray_path}")
        print(f"  Конфиг:   {config_path}")
        print(f"  SOCKS5:   127.0.0.1:{socks_port}")
        print("=" * 50)
        print("  Настройте Telegram:")
        print("  Settings → Data and Storage → Proxy → SOCKS5")
        print(f"  Host: 127.0.0.1  Port: {socks_port}")
        print("=" * 50)
        print("  Ctrl+C для остановки")
        print()

    process = None

    def cleanup(signum=None, frame=None):
        nonlocal process
        if process and process.poll() is None:
            if not args.quiet:
                print("\nОстановка Xray...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            if not args.quiet:
                print("Готово.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        process = subprocess.Popen(
            [xray_path, "run", "-c", config_path],
            stdout=sys.stdout if not args.quiet else subprocess.DEVNULL,
            stderr=sys.stderr if not args.quiet else subprocess.DEVNULL,
            cwd=os.path.dirname(os.path.abspath(xray_path)) or ".",
        )
    except OSError as e:
        print(f"Ошибка запуска Xray: {e}")
        sys.exit(1)

    process.wait()
    if process.returncode != 0 and not args.quiet:
        print(f"Xray завершился с кодом {process.returncode}")
    sys.exit(process.returncode or 0)


if __name__ == "__main__":
    main()
