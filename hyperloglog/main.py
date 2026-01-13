import os
import math
import hashlib
import time


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


def exact_unique_count(ips: list[str]) -> int:
    """
    Точний підрахунок унікальних IP-адрес за допомогою set.
    """
    return len(set(ips))


class HyperLogLog:
    """
    Коректна реалізація HyperLogLog з лінійною корекцією
    для малих наборів даних.
    """

    def __init__(self, p: int = 4) -> None:
        self.p = p                  # кількість біт для індексу
        self.m = 1 << p             # кількість регістрів
        self.registers = [0] * self.m

    @staticmethod
    def _hash(value: str) -> int:
        """
        Стабільний 64-бітний хеш.
        """
        digest = hashlib.sha256(value.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], byteorder="big")

    @staticmethod
    def _rho(w: int, max_bits: int = 64) -> int:
        """
        Кількість ведучих нулів + 1.
        """
        if w == 0:
            return max_bits + 1
        return max_bits - w.bit_length() + 1

    def add(self, value: str) -> None:
        x = self._hash(value)
        index = x >> (64 - self.p)
        w = x << self.p & ((1 << 64) - 1)
        rank = self._rho(w)
        self.registers[index] = max(self.registers[index], rank)

    def count(self) -> float:
        """
        Повертає оцінку кількості унікальних елементів
        з корекцією для малих значень.
        """
        indicator = sum(2.0 ** -r for r in self.registers)
        alpha = 0.673 if self.m == 16 else 0.7213 / (1 + 1.079 / self.m)
        estimate = alpha * self.m * self.m / indicator

        # Лінійна корекція для малих наборів
        zeros = self.registers.count(0)
        if zeros > 0:
            linear_count = self.m * math.log(self.m / zeros)
            return linear_count

        return estimate


def hyperloglog_count(ips: list[str]) -> float:
    """
    Наближений підрахунок унікальних IP-адрес
    з використанням HyperLogLog.
    """
    hll = HyperLogLog(p=4)

    for ip in ips:
        hll.add(ip)

    return hll.count()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    log_path = os.path.join(BASE_DIR, "lms-stage-access.log")

    ips = load_ips_from_log(log_path)

    start = time.time()
    exact_count = exact_unique_count(ips)
    exact_time = time.time() - start

    start = time.time()
    approx_count = hyperloglog_count(ips)
    approx_time = time.time() - start

    print("Результати порівняння:")
    print(f"{'':25}Точний підрахунок   HyperLogLog")
    print(f"Унікальні елементи{exact_count:18.1f}{approx_count:14.1f}")
    print(f"Час виконання (сек.){exact_time:14.4f}{approx_time:14.4f}")
