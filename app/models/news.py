from odmantic import Model


class NewsModel(Model):
    title: str
    originallink: str
    link: str
    description: str
    pubDate: str

    model_config = {"collection": "news"}
