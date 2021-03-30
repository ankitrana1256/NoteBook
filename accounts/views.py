from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Subject
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('user_ip')
        password = request.POST.get('user_key')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "USERNAME OR PASSWORD IS INCORRECT")
    context = {}
    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


# def register_page(request):
#     form = CreateUserForm()
#
#     if request.method == 'POST':
#
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account successfully created')
#     context = {'form': form}
#     return render(request, 'accounts/register-page.html', context)


@login_required(login_url='login')
def home(request):
    sem = request.POST.get('sem')
    if sem != "" and sem is not None:
        subject = Subject.objects.filter(semester__id=sem)
    else:
        subject = Subject.objects.filter(semester__id=1)

    n = len(subject)
    context = {'Subject': subject, 'range': n}
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
def notesview(request, id):
    notes1 = Subject.objects.get(id=id).notes_set.filter(unit__id=1)
    notes2 = Subject.objects.get(id=id).notes_set.filter(unit__id=2)
    notes3 = Subject.objects.get(id=id).notes_set.filter(unit__id=3)
    notes4 = Subject.objects.get(id=id).notes_set.filter(unit__id=4)
    assign = Subject.objects.get(id=id).notes_set.filter(unit__id=5)
    info = Subject.objects.get(id=id)
    context = {'Note1': notes1, 'Note2': notes2, 'Note3': notes3, 'Note4': notes4, 'info': info, 'Assignment':assign}
    return render(request, "accounts/notesview.html", context)


@login_required(login_url='login')
def about(request):
    return render(request, 'accounts/about.html')


@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)


class SignUpView(View):
    form_class = CreateUserForm
    template_name = 'accounts/register-page.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your NoteBook Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            recipent_list = [user.email,]
            send_mail(subject, message, email_from, recipent_list)
            # user.email_user(subject, message)
            messages.success(request, ('Please Confirm your email to complete registration.'))
        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('signup')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('signup')
