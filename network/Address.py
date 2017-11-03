class Address(object):
    """
    Сетевой адрес.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Конструктор

        Args:
            host (str): Хост.
            port (int): Порт.
        """
        super(Address, self).__init__()
        self._host = host
        self._port = port

    def __eq__(self, o: object) -> bool:
        return self.host == o.host and self.port == o.port if isinstance(o, Address) else False

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def host(self) -> str:
        """
        Возвращает хост.

        Returns:
            str: Хост.
        """
        return self._host

    @property
    def port(self) -> int:
        """
        Возвращает порт.

        Returns:
            int: Порт.
        """
        return self._port

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта.
        """
        return '{0}:{1}'.format(self.host, self.port)
