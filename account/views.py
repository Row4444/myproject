from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from account.forms import RegistrationForm, AuthenticationForm
from account.models import User
from account.tasks import send_email_user

from account.tokens import account_activation_token


class Registration(View):
    def get(self, request):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'account/register.html', context)

    def post(self, request):
        context = {}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                password1 = form.cleaned_data.get('password1')
                date_of_birth = form.cleaned_data.get('date_of_birth')

                user = get_object_or_404(User, email=email)
                current_site = get_current_site(request)
                message = render_to_string('account/activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })

                account = authenticate(
                    email=email,
                    password=password1,
                    date_of_birth=date_of_birth,
                )

                login(request, account)

                #

                send_email_user(email=email, token=message)

                return redirect('Q')
            else:
                context['registration_form'] = form

        return render(request, 'account/register.html', context)


class Login(View):
    def get(self, request):
        context = {}
        if request.method == "GET":
            form = AuthenticationForm()
            context['login_form'] = form
            return render(request, 'account/login.html', context)

    def post(self, request):
        context = {}
        user = request.user
        if user.is_authenticated:
            return redirect('Q')
        if request.POST:
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)

                if user:
                    login(request, user)
                    return redirect('Q')
            context['login_form'] = form
            return render(request, 'account/login.html', context)




def activate(request, idb64, token):
    try:
        id = force_text(urlsafe_base64_decode(idb64))
        user = User.objects.get(id=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verificate = True
        user.save()
    return redirect('Q')


def logout_view(request):
    logout(request)
    return redirect('Login')

