from django import forms
from .models import CustomUser, BlogPost, BlogCategory


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title", "image", "category", "summary", "content", "draft")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["summary"].widget = forms.Textarea(attrs={"rows": 4})
        self.fields["content"].widget = forms.Textarea(attrs={"rows": 8})
        self.fields["category"].queryset = BlogCategory.objects.all()

    def clean_category(self):
        category_instance = self.cleaned_data["category"]
        if not category_instance:
            raise forms.ValidationError("Please select a category")
        return category_instance

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
