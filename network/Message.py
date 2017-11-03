"""
В этом модуле описывается класс NetworkMessage.
"""
from .Address import Address


class Message(object):
    """
    Сообщение, передающееся по сети.
    """

    def __init__(
            self,
            address_from: Address,
            address_to: Address
    ):
        """
        Конструктор.

        Args:
            address_from (Address): Адрес отправителя.
            address_to (Address): Адрес получателя.
        """
        super(Message, self).__init__()
        self._address_from = address_from
        self._address_to = address_to

    @property
    def address_from(self) -> Address:
        """
        Возвращает адрес отправителя.

        Returns:
            Address: Адрес отправителя.
        """
        return self._address_from

    @property
    def address_to(self) -> Address:
        """
        Возвращает адрес получателя.

        Returns:
            Address: Адрес получателя.
        """
        return self._address_to

    def __str__(self):
        return 'from {a_from} to {a_to}'.format(a_from=self.address_from, a_to=self.address_to)
