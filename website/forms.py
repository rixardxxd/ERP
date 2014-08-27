# -*- coding: utf-8 -*-
# coding=gbk1
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField(label=_(u"邮箱"), required=True)
    password = forms.CharField(label=_(u"密码"), widget=forms.PasswordInput, required=True)

    error_messages = {
        'invalid_login': _(u"邮箱或者密码不正确"),
        'inactive': _(u"该账号已经停用"),
    }

    user_cache = None

    def clean(self):
        super(LoginForm, self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                self.user_cache = authenticate(username=user.username,
                                               password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class SignupForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _(u"邮箱已经存在"),
        'password_mismatch': _(u"密码不符"),
    }

    first_name = forms.CharField(required=False, max_length=100, label=u'名字:')
    last_name = forms.CharField(required=False, max_length=100, label=u'姓氏:')
    email = forms.EmailField(required=True, label=_(u"邮箱"))
    password1 = forms.CharField(label=_(u"密码"),
        widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_(u"确认密码"),
        widget=forms.PasswordInput, required=True,
        help_text=_("Enter the same password as above, for verification."))

    def clean_email(self):
        #this check whether the email address exists.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        #django only allow max 30 chars for the username
        username = email
        if email and len(email) > 30:
            username = email[0:30]
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        if commit:
            user.save()

        #do the authentication
        user_cache = authenticate(username=user.username,
                                           password=password)
        if user_cache is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        elif not user_cache.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        return user_cache

