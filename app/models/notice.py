from odmantic import Model
from datetime import datetime


class NoticeModel(Model):
    title: str
    content: str
    create_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = {"collection": "notice"}
