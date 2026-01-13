class BloomFilter:
    """
    Реалізація фільтра Блума для перевірки наявності елементів.
    Дозволяє зберігати велику кількість значень з мінімальним
    використанням памʼяті за рахунок імовірнісної природи.
    """

    def __init__(self, size: int, num_hashes: int) -> None:
        """
        Ініціалізація фільтра Блума.

        :param size: розмір бітового масиву
        :param num_hashes: кількість хеш-функцій
        """
        if size <= 0 or num_hashes <= 0:
            raise ValueError("Розмір та кількість хешів повинні бути додатними")

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _hashes(self, item: str):
        """
        Генерує послідовність хеш-індексів для елемента.

        :param item: значення для хешування
        :return: генератор індексів у бітовому масиві
        """
        for i in range(self.num_hashes):
            combined = f"{item}:{i}"
            yield hash(combined) % self.size

    def add(self, item: str) -> None:
        """
        Додає елемент до фільтра Блума.

        :param item: значення для додавання
        """
        if not isinstance(item, str):
            return

        for index in self._hashes(item):
            self.bit_array[index] = True

    def contains(self, item: str) -> bool:
        """
        Перевіряє, чи може елемент бути присутнім у фільтрі.

        :param item: значення для перевірки
        :return: True — можливо присутній, False — точно відсутній
        """
        if not isinstance(item, str):
            return False

        return all(self.bit_array[index] for index in self._hashes(item))
