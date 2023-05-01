from django.core.mail import send_mail


def send_password_reset_email(email, token):
    subject = 'Password reset'

    message = f'Use this link to reset your password: https://mail-sender.vingb.com/custom-mail/edf554f6-c207-4ec7-a657-9285913a9a35{token}'

    from_email = 'muhammediyadiyad@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

