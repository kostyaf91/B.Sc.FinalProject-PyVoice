from django.forms import ModelForm,HiddenInput,TextInput,EmailInput,DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import account, invoice_detail


class CreateUserForm(UserCreationForm):
    class Meta:
        model = account
        fields = [
            'username',
            'password1',
            'password2',
            'business_Name',
            'business_Email',
            'business_Address',
            'business_Phone',
            'business_Number'

        ]


class InvoiceForm(ModelForm):
    class Meta:
        model = invoice_detail
        widgets = {
            'user': HiddenInput(),
            # 'amounts': HiddenInput(),
            # 'table_Items': HiddenInput(),
            'client_Name': TextInput(attrs={'placeholder': 'client_Name'}),
            'client_Email': EmailInput(attrs={'placeholder': 'client_Email'}),
            'client_Address': TextInput(attrs={'placeholder': 'client_Address'}),
            'client_Phone': TextInput(attrs={'placeholder': 'client_Phone'}),

            'invoice_Number': TextInput(attrs={'placeholder': 'invoice_Number'}),
            'date': DateInput(attrs={'placeholder': 'date'}),
            'terms': TextInput(attrs={'placeholder': 'terms'}),

        }

        fields = '__all__'
