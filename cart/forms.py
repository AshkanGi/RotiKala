from django import forms
from .models import Address

widget = forms.TextInput(attrs={'class': 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 placeholder-transparent focus:outline-none focus:ring-0'})


class AddAddressForm(forms.Form):
    full_name = forms.CharField(max_length=60, widget=widget)
    phone = forms.CharField(max_length=11, widget=widget)
    address = forms.CharField(widget=widget)
    city = forms.CharField(max_length=20, widget=widget)
    province = forms.CharField(max_length=20, widget=widget)
    zip_code = forms.CharField(max_length=20, widget=widget)

    def save(self, user):
        address = Address(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            province=self.cleaned_data['province'],
            zip_code=self.cleaned_data['zip_code']
        )
        address.save()
        return address


