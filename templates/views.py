# Create your views here.


from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')