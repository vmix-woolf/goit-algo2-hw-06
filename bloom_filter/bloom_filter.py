class BloomFilter:
    def __init__(self, size: int, num_hashes: int) -> None:
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _hashes(self, item: str):
        for i in range(self.num_hashes):
            yield hash(f"{item}:{i}") % self.size

    def add(self, item: str) -> None:
        if not isinstance(item, str):
            return
        for index in self._hashes(item):
            self.bit_array[index] = True

    def contains(self, item: str) -> bool:
        if not isinstance(item, str):
            return False
        return all(self.bit_array[index] for index in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    results = {}

    for password in passwords:
        if not isinstance(password, str) or password == "":
            results[password] = "некоректне значення"
            continue

        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results
