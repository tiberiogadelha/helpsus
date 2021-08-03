from core.models import FichaHandler

class Util():

    def getFicha(self) -> int:
        ficha = FichaHandler.objects.filter(id = 1).first()
        ficha.num += 1
        ficha.save()
        return ficha.num + 1

    def resetFicha(self):
        ficha = FichaHandler.objects.filter(id = 1).first()
        ficha.num += 1
        ficha.save()