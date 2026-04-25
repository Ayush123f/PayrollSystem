from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_pw  = request.POST.get('old_password')
        new_pw1 = request.POST.get('new_password1')
        new_pw2 = request.POST.get('new_password2')
        if new_pw1 != new_pw2:
            messages.error(request, 'New passwords do not match.')
        elif not request.user.check_password(old_pw):
            messages.error(request, 'Old password is incorrect.')
        else:
            request.user.set_password(new_pw1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
    return render(request, 'accounts/change_password.html')