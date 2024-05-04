from django import forms
from .models import UserProfile

class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Select a profile image',required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields =["profile_image"]
        
# class EnquiryForm(ModelForm):
#     class Meta:
#         model = Enquiry
#         fields = ['first_name', 'last_name', 'email', 'contact', 'message']