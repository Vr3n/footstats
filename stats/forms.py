from time import sleep
from django.core.mail import send_mail
from django import forms

from stats.tasks import send_feedback_email_task


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="message",
        widget=forms.Textarea(attrs={'rows': 5})
    )

    def send_email(self):
        send_feedback_email_task.delay(
            email_address=self.cleaned_data['email'],
            message=self.cleaned_data['message']
        )
