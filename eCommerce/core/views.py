from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator

from item.models import Category, Item
from .forms import SignUpForm, LogInForm

def contact(request):
    return render(request, 'core/contact.html')

def index(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        p = Paginator(Item.objects.filter(is_sold=False).exclude(created_by=request.user), 5)
    else:
        p = Paginator(Item.objects.filter(is_sold=False), 5)
    page = request.GET.get('page')
    items_pages = p.get_page(page)

    context = {
        'categories': categories,
        'pages': items_pages,
    }
    return render(request, 'core/index.html', context=context)

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'core/signUp.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, self.template_name, {'form': form})

class LogInView(LoginView):
    template_name = 'core/logIn.html'
    authentication_form = LogInForm

class LogOutView(LogoutView):
    redirect_field_name ='/'