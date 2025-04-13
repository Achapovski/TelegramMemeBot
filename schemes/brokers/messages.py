from pydantic import BaseModel


class DeliveryMessageScheme(BaseModel):
    pass


class DeliveryDelMessageScheme(DeliveryMessageScheme):
    chat_id: int | str
    message_ids: list[int] | tuple[int]
