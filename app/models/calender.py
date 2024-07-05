from odmantic import Model


class CalenderModel(Model):
    month: str
    date: str
    time: str
    game: str
    tv: str
    stadium: str
    note: str
    home_team: str

    model_config = {"collection": "calender"}
