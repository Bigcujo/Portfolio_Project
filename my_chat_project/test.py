from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        'Test Email Subject',
        'This is the body of the test email.',
        'your-email@gmail.com',
        ['kinggriffinmike@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent!")
