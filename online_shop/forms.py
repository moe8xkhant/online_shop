from django import forms
from models import CustomerProfile, Products
from django.core.validators import validate_email
import re

class customer_data_form(forms.ModelForm):

    first_name = forms.CharField(max_length=100, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    email = forms.CharField(max_length=255, required=True, help_text='Required.')
    password = forms.CharField(max_length=255, required=True, help_text='Required.')
    password_repeat = forms.CharField(max_length=255, required=True, help_text='Required.')

    class Meta:
        model = CustomerProfile
        fields = ('phone_no',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
            return email
        except:
            raise forms.ValidationError("Email is not valid.")

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) > 25:
            raise forms.ValidationError('Password maximum length must be 25.')

        count = 0
        pwd_length = len(password)

        # Check if contains at least one digit
        if re.search(r'\d', password):
            count += 1

        # Check if contains at least one uppercase letter
        if re.search(r'[A-Z]', password):
            count += 1

        # Check if contains at least one lowercase letter
        if re.search(r'[a-z]', password):
            count += 1

        # Check if contains at least one special character
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:-]')
        if (string_check.search(password) == None):
            pass
        else:
            count += 1

        if pwd_length < 10 or count < 4:
            raise forms.ValidationError(
                'Password must contain a minimum of 10 characters including at least one number, one UPPER and one lower case character, one special character.')

        return password

    def clean_password_repeat(self):

        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_repeat')

        if len(password2) > 25:
            raise forms.ValidationError('Password maximum length must be 25.')

        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')

        if phone_no:
            if len(phone_no) > 15:
                raise forms.ValidationError('Phone no maximum length must be 15.')
            if not str(phone_no).isdigit():
                raise forms.ValidationError('Phone no is invalid.')

        return phone_no

class product_data(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Products.objects.filter(name=name):
            raise forms.ValidationError('Product Name already exists.')
        return name

class product_edit(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"

