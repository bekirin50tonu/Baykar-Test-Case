# Create your views here.


from django.shortcuts import render

# giriş yapılacak sayfası getirecek fonksiyon tanımı.
def login_page(request):
    return render(request, 'login.html')

# üretim yapılacak sayfası getirecek fonksiyon tanımı.
def dashboard_page(request):
    return render(request, 'dashboard.html')

# montaj yapılacak sayfası getirecek fonksiyon tanımı.
def montage_page(request):
    return render(request,"montage.html")