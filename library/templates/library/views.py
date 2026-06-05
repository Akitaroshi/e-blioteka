from django.shortcuts import render

def main_landing(request):
    return render(request, 'library/main_landing.html')
