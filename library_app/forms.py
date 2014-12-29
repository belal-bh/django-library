from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from .models import UserProfile, User, Author, Publisher, LendPeriods, Book
from django.utils import timezone
from django.forms import ModelForm


class UserEditForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=False, widget=forms.widgets.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))

    mobile = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Mobile No.'}))
    website = forms.CharField(required=True, widget=forms.widgets.URLInput(attrs={'placeholder': 'Website address'}))


    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile', 'website']

    def is_valid(self):
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return self

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(
                'This email address is already in use. Please supply a different email address.')
        return email

    def save(self, user):
        # print '%s' % self.cleaned_data['username']
        # user = User.objects.filter(username=self.cleaned_data['username'])[0]
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.mobile = self.cleaned_data['mobile']
        user.profile.website = self.cleaned_data['website']
        user.profile.save()
        user.save()
        return user


class UserCreateForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    # username = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    # mobile = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Mobile number'}))
    # website = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Website url'}))


    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    def save(self):
        user = super(UserCreateForm, self).save()
        user_profile = UserProfile(user=user, join_date=timezone.now())
        user_profile.save()
        return user_profile

    class Meta:
        fields = ['username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'date_of_birth', 'id']
        widgets = {
            'name': forms.widgets.TextInput(attrs={'placeholder': 'Name'}),
            'surname': forms.widgets.TextInput(attrs={'placeholder': 'Surname'}),
            'date_of_birth': forms.widgets.DateInput(attrs={'placeholder': 'Date of birth'}),
            'id': forms.widgets.HiddenInput(),
        }


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
        widgets = {
            'name': forms.widgets.TextInput(attrs={'placeholder': 'Name'}),
            }


class LendPeriodForm(ModelForm):
    class Meta:
        model = LendPeriods
        fields = ['name', 'days_amount']
        widgets = {
            'name': forms.widgets.TextInput(attrs={'placeholder': 'Name'}),
            'days_amount': forms.widgets.TextInput(attrs={'placeholder': 'Amount of days'}),
            }


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'ISBN', 'publisher', 'author', 'lend_period', 'page_amount']
        widgets = {
            'title': forms.widgets.TextInput(attrs={'placeholder': 'Title'}),
            'ISBN': forms.widgets.TextInput(attrs={'placeholder': 'ISBN'}),
            'publisher': forms.widgets.Select(),
            'author': forms.widgets.Select(attrs={'placeholder': 'Author'}),
            'lend_period': forms.widgets.Select(attrs={'placeholder': 'Lend period'}),
            'page_amount': forms.widgets.NumberInput(attrs={'min': 0, 'placeholder': 'Amount of pages'}),
            }
