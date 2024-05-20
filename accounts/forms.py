from django import forms
from .models import  UserProfile, feedback
from .models import Inquiry

class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Select a profile image',required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields =["profile_image"]
        


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['subject', 'inquiry']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'inquiry': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control'}),
        }