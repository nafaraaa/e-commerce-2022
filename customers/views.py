from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.db import transaction
import secrets
import smtplib
from .models import UserProfile
from .forms import FormSignUp,FormLogIn


@csrf_protect
def registerPage(request):
    # inisialisasi form (kosong untuk request GET, terisi untuk POST)
    form = FormSignUp()
    
    if request.method == 'POST':
        # hubungkan form dengan data POST
        form = FormSignUp(request.POST)
        
        if form.is_valid():
            try:
                # memulai transaksi atomik untuk memastikan konsistensi data
                with transaction.atomic():
                    print("Form has been posted and is valid")
                    
                    user = form.save()
                    
                    # membuat atau fetch userprofile dan membuat kode verifikasi
                    profile, created = UserProfile.objects.get_or_create(user=user)
                    verification_code = f"{secrets.randbelow(10**6):06d}"
                    profile.verification_code = verification_code
                    profile.code_created_at = timezone.now()
                    profile.save()
                    
                    # mengirim email verifikasi
                    send_mail(
                        'Verify Your Email',
                        f'Your verification code: {verification_code}',
                        'noreply@yourdomain.com',
                        [user.email],
                        fail_silently=False,
                    )
                    
                    # login user dan redirect ke verify.html
                    login(request, user)
                    return redirect('verify_email')
                    
            except smtplib.SMTPException as e:
                # Handle SMTP email sending errors
                error_message = "Gagal mengirimkan Email verifikasi."
                if "550" in str(e):
                    error_message += " Email tidak valid atau tidak ditemukan."
                else:
                    error_message += " Coba lagi nanti, atau hubungi admin."
                
                messages.error(request, error_message)
                # menghapus user jika email gagal dikirim
                if user:
                    user.delete()
                return redirect('register')
                
            except Exception as e:
                # handle error lain
                messages.error(request, "Terjadi kesalahan sistem. Silahkan coba lagi.")
                print(f"Unexpected error during registration: {str(e)}")
                # menghapus user jika ada error
                if 'user' in locals() and user:
                    user.delete()
                return redirect('register')
                
        else:
            # form tidak valid, kirim error message
            print("Form is not valid")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        print("Loading registration page (GET request)")
    
    # menyiapkan context dan render template
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def loginPage(request):
    form = FormLogIn()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.userprofile.email_verified:
                messages.warning(request, 'Please verify your email first')
                return redirect('verify_email')
            
            login(request, user)
            return redirect('homey:index')
        else:
            messages.error(request, 'Invalid credentials')
    
    context = {'form':form}
    return render(request,'registration/login.html', context)

@login_required
def logoutPage(request):
	logout(request)
	return redirect('login')

@login_required
def verify_email(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "Profil tidak ditemukan. Silahkan daftar ulang.")
        return redirect('register')
    
    if profile.email_verified:
        return redirect('homey:index')

    if request.method == 'POST':
        entered_code = request.POST.get('code', '').strip()
        if entered_code == profile.verification_code:
            if (timezone.now() - profile.code_created_at).total_seconds() <= 86400:
                profile.email_verified = True
                profile.save()
                messages.success(request, 'Email verified!')
                return redirect('homey:index')
            else:
                messages.error(request, "Kode sudah kedaluarsa. Silahkan minta resend")
                return redirect('resend_verification')
        else:
            messages.error(request, 'Invalid code')
    return render(request, 'registration/verify.html')

@login_required
def resend_verification(request):
    profile = request.user.userprofile
    new_code = f"{secrets.randbelow(10**6):06d}"
    profile.verification_code = new_code
    profile.code_created_at = timezone.now()
    profile.save()
    send_mail(
        'New Verification Code',
        f'Your new code: {new_code}',
        'noreply@example.com',
        [request.user.email],
        fail_silently=False,
    )
    messages.info(request, 'Kode baru telah dikirim ke email Anda')
    return redirect('verify_email')
