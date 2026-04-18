from teamup.domain import IMessageRepository, Message

from ....exceptions import MessageCreationError


class SendMessageUseCase:
    def __init__(self, mes_r: IMessageRepository):
        self._mes_r = mes_r

    async def __call__(self, message: Message) -> Message:
        new_message = await self._mes_r.create(message)
        if new_message is None:
            raise MessageCreationError("Ошибка отправки сообщения")

        return new_message
