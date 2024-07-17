from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "address_line1",
            "city",
            "state",
            "pincode",
            "is_patient",
            "is_doctor",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        is_patient = cleaned_data.get("is_patient")
        is_doctor = cleaned_data.get("is_doctor")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

        if is_patient and is_doctor:
            raise forms.ValidationError(
                "You cannot select both Patient and Doctor roles. Please choose one."
            )

        if not is_patient and not is_doctor:
            raise forms.ValidationError(
                "You must select either Patient or Doctor role."
            )

        return cleaned_data
