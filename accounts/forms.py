from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

class UserCustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):      # Meta 클래스도 상속받을수 있다.
        model = get_user_model()
        fields = ['username', 'email',]
    
class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name',]
        
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction']