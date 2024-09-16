from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import ( LoginView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile, CustomUser
from blog.models import Post
from django.views.generic import ListView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm

#creat views for the user app

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully for {user_name}!, You can login now')
            form.save()
            return redirect('user-login')  # Redirect to 'blog-home' upon successful registration
        else:
            # Log form errors for debugging purposes
            print("Form is invalid")
            print(form.errors)
    else:
        # For GET requests, instantiate a new, empty form
        form = UserRegistrationForm()
        print("GET request")

    # Render the registration template with the form
    return render(request, 'user/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('blog-home')
    

class UserPostListView(ListView):
    model = Post
    template_name = 'user/user_posts.html'
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    


class UserPasswordResetView(PasswordResetView):
    template_name = "user/password_reset.html"
    email_template_name = "user/password_reset_email.html"
    subject_template_name = "user/password_reset_subject.txt"
    success_url = reverse_lazy('password_reset_done')
    token_generator = default_token_generator
    form_class = PasswordResetForm
    from_email = None


    def get_email_context(self, user):
        """
        Add extra context for the email.
        """
        context = {
            'email': user.email,
            'domain': self.request.META['HTTP_HOST'],
            'site_name': 'Your Site Name',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': self.token_generator.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http',
        }
        context['reset_url'] = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={
                'uidb64': context['uid'],
                'token': context['token'],
            })
        )
        return context

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def form_valid(self, form):
        """
        If the form is valid, override to include custom email context.
        """
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
        }
        for user in form.get_users(form.cleaned_data['email']):
            context = self.get_email_context(user)
            self.send_mail(
                self.subject_template_name, 
                self.email_template_name,
                context, 
                opts['from_email'], 
                user.email,
                html_email_template_name=self.html_email_template_name,
            )
        return super().form_valid(form)


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user/password_reset_confirm.html"
    success_url = reverse_lazy('password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'


@login_required
def profile(request):
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user-profile')
    else: 
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()


    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'user/profile.html', context)



    



