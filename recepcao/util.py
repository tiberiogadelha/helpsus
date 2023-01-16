import datetime

from pytz import timezone

from core.models import FichaHandler
from helpSUS.settings import TIME_ZONE


class Util():

    def getFicha(self) -> int:
        ficha = FichaHandler.objects.filter(id=1).first()
        ficha.num += 1
        ficha.save()
        return ficha.num + 1

    def resetFicha(self):
        ficha = FichaHandler.objects.filter(id=1).first()
        ficha.num += 1
        ficha.save()

    @staticmethod
    def agora():
        localtz = timezone(TIME_ZONE)
        return localtz.localize(datetime.datetime.now())
