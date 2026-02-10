import logging
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from .models import User, EmailVerificationToken

logger = logging.getLogger(__name__)


def register_view(request):
    """
    User registration view with email verification.
    
    Flow:
    1. User fills registration form
    2. User account created with is_email_verified=False
    3. Verification email sent with unique token
    4. User must click link to verify email
    """
    if request.user.is_authenticated:
        return redirect('flights:list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create user but don't activate yet
            user = form.save(commit=False)
            user.is_active = True
            user.is_email_verified = False
            user.save()

            # Generate and send verification token
            token = secrets.token_urlsafe(32)
            EmailVerificationToken.objects.create(user=user, token=token)

            # Send verification email
            verification_link = request.build_absolute_uri(
                f'/accounts/verify-email/{token}/'
            )
            send_mail(
                subject='Verify Your Email - Airline Booking',
                message=f'Please verify your email by clicking the link: {verification_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            logger.info(f'User {user.username} registered. Verification email sent to {user.email}')
            return redirect('accounts:verification_pending', username=user.username)
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request, token):
    """
    Email verification view.
    
    User clicks link from verification email containing unique token.
    Upon successful verification, account becomes fully active.
    """
    try:
        email_token = EmailVerificationToken.objects.get(token=token)

        if email_token.is_used:
            logger.warning(f'Attempted to use already-used token: {token}')
            return render(request, 'accounts/verification_error.html', 
                        {'error': 'This verification link has already been used.'})

        if email_token.is_expired():
            logger.warning(f'Attempted to use expired token for user {email_token.user.username}')
            return render(request, 'accounts/verification_error.html',
                        {'error': 'This verification link has expired. Please register again.'})

        # Mark email as verified
        user = email_token.user
        user.is_email_verified = True
        user.save()

        email_token.is_used = True
        email_token.save()

        logger.info(f'Email verified for user {user.username}')
        return render(request, 'accounts/verification_success.html', {'user': user})

    except EmailVerificationToken.DoesNotExist:
        logger.warning(f'Invalid verification token: {token}')
        return render(request, 'accounts/verification_error.html',
                    {'error': 'Invalid verification token.'})


def verification_pending_view(request, username):
    """
    Display message to user indicating verification email was sent.
    """
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/verification_pending.html', {'user': user})


def login_view(request):
    """
    User login view with session management.
    
    Logs user login attempt and success.
    Only allows login if email is verified.
    """
    if request.user.is_authenticated:
        return redirect('flights:list')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Check if email is verified
            if not user.is_email_verified:
                logger.warning(f'Login attempt with unverified email: {user.username}')
                return render(request, 'accounts/login.html',
                            {'form': form, 'error': 'Please verify your email before logging in.'})

            login(request, user)
            logger.info(f'User {user.username} logged in from IP {get_client_ip(request)}')
            return redirect('flights:list')
        else:
            logger.warning(f'Failed login attempt')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view with session termination.
    
    Logs user logout and terminates session.
    """
    username = request.user.username
    logout(request)
    logger.info(f'User {username} logged out')
    return redirect('accounts:login')


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip