from django.shortcuts import render
from django.http import HttpResponse

def study_companion(request):
    return HttpResponse('Estou em study companion')