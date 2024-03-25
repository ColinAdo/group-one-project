from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser, Vendor

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "profile_picture",
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ["name", "description", "contact",
                  "address", "warranty_period", "shipping_on_time"]
