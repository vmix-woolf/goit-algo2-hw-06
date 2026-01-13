import os

def is_valid_ipv4(ip: str) -> bool:
    """
    Перевіряє, чи є рядок коректною IPv4-адресою.
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False
        value = int(part)
        if value < 0 or value > 255:
            return False

    return True


def load_ips_from_log(file_path: str) -> list[str]:
    """
    Завантажує IP-адреси з лог-файлу.
    Некоректні рядки ігноруються.
    """
    ips: list[str] = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            ip = parts[0]
            if is_valid_ipv4(ip):
                ips.append(ip)

    return ips


if __name__ == "__main__":
    # Тимчасова перевірка роботи завантаження
    BASE_DIR = os.path.dirname(__file__)
    log_path = os.path.join(BASE_DIR, "lms-stage-access.log")

    ips = load_ips_from_log(log_path)
    print(f"Завантажено IP-адрес: {len(ips)}")
