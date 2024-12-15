from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User,Category
from .models import Department,Grievance ,Priority



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )


    class Meta:
        model = User
        fields = ["email", "phone"]


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """


    password = ReadOnlyPasswordHashField()


    class Meta:
        model = User
        fields = ["email", "password", "phone", "is_active", "is_admin"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Add any custom validation for the username, if needed
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Add any custom validation for the password, if needed
        return password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")



class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['user','title', 'description', 'priority', 'department', 'category']
        

    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), empty_label="Select Priority")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department", label="Department")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", label="Category")

