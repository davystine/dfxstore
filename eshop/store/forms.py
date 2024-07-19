from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile, Rating
from django import forms



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address', 'style':'margin-bottom: 10px;'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name', 'style':'margin-bottom: 10px;'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name', 'style':'margin-bottom: 10px;'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted small">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['password1'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password must contain at least 8 characters.</li><li>It can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted small">Enter the same password for verification.</span>'


class AccountInfoForm(UserChangeForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address', 'style':'margin-bottom: 10px;'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name', 'style':'margin-bottom: 10px;'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name', 'style':'margin-bottom: 10px;'}))
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super(AccountInfoForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted small">Required. 150 characters or fewer.</span>'
        

class UpdatePasswordForm(SetPasswordForm):   
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['new_password1'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password must contain at least 8 characters.</li><li>It can\'t be entirely numeric.</li></ul>'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'
        self.fields['new_password2'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted small">Enter the same password for verification.</span>'


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label="", max_length=15, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    address1 = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 1'}))
    address2 = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2'}))
    city = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    state = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    zipcode = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}))
    country = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    birthday = forms.DateField(label="Birthday", required=False, widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'Birthday', 'type':'date'}))
    gender = forms.ChoiceField(label="Gender", choices=UserProfile.GENDER_CHOICES, required=False, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Gender'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', 'birthday', 'gender']


class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
