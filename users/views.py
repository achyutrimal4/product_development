from email import message
from lib2to3.pgen2 import token
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm, UsersAuthenticationForm, ProfileUpdateForm, ContactForm, MessageForm, ContactReplyForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ContactMail, Profile, Inbox
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def register_view(request):

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            messages.success(
                request, 'Account created. Please check your inbox and verify your email to continue.')
            return redirect('login')
        else:
            context['registration_form'] = form
    else:  # GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'users/register.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('admin_panel')
        else:
            return redirect('home')

    if request.method == "POST":
        form = UsersAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('admin_panel')
                    else:
                        return redirect('home')
                else:
                    messages.error(
                        request, 'Please verify your email address to login.')

    else:
        form = UsersAuthenticationForm()

    context['login_form'] = form
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'User was successfully logged out.')
    return redirect('landing_page')


@login_required(login_url='login')
def profile_view(request):
    user_profile = request.user.profile
    User = get_user_model()
    admin = User.objects.order_by('-is_admin').first()
    context = {'user_profile': user_profile, 'admin': admin}
    return render(request, 'users/users_profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    context = {'form': form}
    return render(request, 'users/editProfile.html', context)

# =================================================================
# Functions to view and respond to password reset requests


# to view all the inbox from users
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def inbox(request):
    page = 'inbox'
    profile = request.user.profile
    inbox = profile.messages.all()
    inbox_count = inbox.count()
    unread_count = inbox.filter(is_read=False).count()
    context = {'inbox': inbox, 'inbox_count': inbox_count,
               'unread_count': unread_count, 'page': page}
    return render(request, 'users/inbox.html', context)

# delete password reset request 
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_reset_inbox(request, pk):
    inbox = Inbox.objects.get(pk=pk)
    if request.method == 'POST':
        inbox.delete()
        messages.success(request, 'Inbox deleted successfully')
        return redirect('inbox')
    
    context = {'inbox': inbox}
    return render(request, 'videos_app/delete_confirmation.html', context)

# =================================================================
# function to create reset requests for users and notify admin


@login_required(login_url='login')
def create_message(request, pk):
    form = MessageForm()

    User = get_user_model()
    admin = User.objects.get(id=pk)
    admin_id = admin.profile.id
    admin_profile = Profile.objects.get(id=admin_id)
    recipient = admin_profile
    sender = request.user.profile

    if request.method == 'POST':
        form = MessageForm()

        message = form.save(commit=False)
        message.sender = sender
        message.receiver = recipient

        message.name = sender.name
        message.email = sender.email

        message.save()
        messages.success(
            request, 'Password reset request was successfully sent.')
        return redirect('myprofile')
    context = {'admin': admin, 'form': form, 'admin_id': admin_id}
    return render(request, 'users/messageForm.html', context)


# =============================================================
# this view is used to read password reset request and to reset the user password.
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def viewMessage(request, pk):
    profile = request.user.profile
    inbox = profile.messages.get(id=pk)
    if inbox.is_read == False:
        inbox.is_read = True
        inbox.save()

    if request.method == 'POST':
        user_email = request.POST['email']
        User = get_user_model()
        try:
            user = User.objects.get(email=user_email)
        except:
            messages.error(request, 'Invalid email address provided')
        new_pass = get_random_string(length=8)
        ctx = {'password': new_pass}

        subject = 'Password Reset'
        body = render_to_string("users/password_reset_confirmation.html", ctx)
        # body = f'Your password has been successfully reset. Your new password is {new_pass} You can use this password to login. Click this link to set new password. '

        msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                             to=[user_email], body=body)

        msg.attach_alternative(body, "text/html")
        msg.send()

        # send_mail(
        #     subject,
        #     body,
        #     settings.EMAIL_HOST_USER,
        #     [user_email],
        #     fail_silently=False,
        # )
        user.set_password(new_pass)
        user.is_pass_reset = True
        user.save()
        messages.success(request, 'New password successfully sent.')
        return redirect('inbox')

    context = {'inbox': inbox}
    return render(request, 'users/message.html', context)


# =============================================================================
#  contact form for logged in and un-logged users /// admin can see the message in their inbox
def contact(request):
    User = get_user_model()

    form = ContactForm()
    context = {}
    admin = User.objects.order_by('-is_admin').first()
    admin_id = admin.profile.id
    admin_profile = Profile.objects.get(id=admin_id)

    recipient = admin_profile
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(
                request, 'Message successfully sent. We\'ll get back to you soon.')
            return redirect('myprofile')
        else:
            messages.error(
                request, 'Message could not be sent. Please try again')
            form = ContactForm(request.POST)
    context = {'admin': admin, 'form': form, 'admin_id': admin_id}
    return render(request, 'users/contact.html', context)


# =================================================================
# function to view all contact messages from users
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def contact_inbox(request):
    page = 'contact_inbox'
    profile = request.user.profile
    inbox = profile.contact_mails.all()
    inbox_count = inbox.count()
    unread_count = inbox.filter(is_read=False).count()
    context = {'page': page, 'inbox': inbox,
               'unread_count': unread_count, 'inbox_count': inbox_count}
    return render(request, 'users/inbox.html', context)


# ===============================
# function to view specific inbox in detail and send reply to the user
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def viewContactMail(request, pk):

    form = ContactReplyForm()
    context = {}
    User = get_user_model()
    if request.method == 'POST':
        form = ContactReplyForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            reply = request.POST['message']
            receiver_mail = request.POST['receiver']
            if User.objects.filter(email=receiver_mail).exists():
           
                subject = 'Thanks for contacting us. Regarding your query...'
                send_mail(
                    subject,
                    reply,
                    settings.EMAIL_HOST_USER,
                    [receiver_mail],
                    fail_silently=False,
                )
                message.save()
                messages.success(request, 'Reply successfully sent.')
                form = ContactReplyForm()
                return redirect('contact-inbox')
            else:
                messages.error(request, 'Email not found.')
        else:
            messages.error(request, 'Reply could not be sent.')
            form = ContactReplyForm(request.POST)

    profile = request.user.profile
    inbox = profile.contact_mails.get(id=pk)
    if inbox.is_read == False:
        inbox.is_read = True
        inbox.save()
    context = {'inbox': inbox, 'form': form, }
    return render(request, 'users/view_contact_mail.html', context)

# ======================================================================
# function to change password after admin resetting user password


@login_required(login_url='login')
def change_password(request):
    User = get_user_model()
    username = request.user.username
    user = User.objects.get(username=username)
    
    
    context = {}
    if request.method == 'POST':
      

        current_pass = request.POST['current-password']
        new_pass = request.POST['new-password']
        confirm_pass = request.POST['confirm-password']

        if (len(current_pass) == 0 or len(new_pass) == 0 or len(confirm_pass) == 0):
            messages.error(request, 'Password field/s cannot be empty.')

        elif not user.check_password(current_pass):
            messages.error(request, 'Current password is incorrect.')

        elif len(new_pass) < 8:
            messages.error(
                request, 'New password must be at least 8 characters.')

        elif current_pass == new_pass:
            messages.error(
                request, 'New password cannot be the same as current password.')

        elif new_pass == confirm_pass:
            user.is_pass_reset = False
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Password successflly changed.')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(
                request, 'Could not change password. Try Again.')

    return render(request, 'users/change_password.html', context)

