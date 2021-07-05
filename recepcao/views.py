from django.shortcuts import render


def mainRecepcao(request):
    return render(request, 'main.html')