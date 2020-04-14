from django.shortcuts import redirect, render

# Create your views here.
def my_login(request):
    return render(request, template_name='login.html')