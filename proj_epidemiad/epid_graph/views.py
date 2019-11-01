from django.shortcuts import render
from django.http import HttpResponse

try:
    import epidemiad
    ep_models=["sir","sir_dem","influenza"]
except ImportError:
    import epidemia
    ep_models = ["sir"]
def index(request):
    return HttpResponse("Hello, world. You're at the epid_graph index.")