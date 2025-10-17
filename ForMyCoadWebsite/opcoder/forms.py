from django import forms
from .models import UserFeedback


class FeedbackForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please provide detailed feedback...'}),
        label='Your Detailed Feedback / Issue'
    )

    class Meta:
        model = UserFeedback
        fields = ['subject', 'message', 'category', 'rating', 'name', 'email']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Bug on Blog Page, Feature Request'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email for Follow-up (Optional)'}),
        }
