from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap3_datetime.widgets import DateTimePicker
from captcha.fields import ReCaptchaField
from registration.models import *
from django.forms.models import ModelForm
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget


user_widgets = {
    'user_first_name': forms.TextInput(attrs={'placeholder':_('First Name'), 'required': True}),
    'user_dob': DateTimePicker(options={"getUTCDate": True, "pickTime": True,
                                              "date":"fa fa-calendar", "viewMode":'years',
                                              "format":'DD/MM/YYYY'},
                                     attrs={'placeholder':_('DD/MM/YYYY'), 'required': True, 'class':'datepicker'}),
    'user_last_name': forms.TextInput(attrs={'placeholder':_('Last Name'),
                                             'required': True}),
    'email': forms.TextInput(attrs={'placeholder':_('Your Email address'),
                                             'required': True}),
    'username': forms.TextInput(attrs={'placeholder':_('Username'),
                                             'required': True}),
}

user_extra_widgets = {
    'user_github'    : forms.TextInput(attrs={'placeholder':_('Github profile'), 'required': False}),
    'user_linkedin'  : forms.TextInput(attrs={'placeholder':_('Linkedin profile'), 'required': False}),
    'user_bio'    :  forms.Textarea(attrs={'placeholder':_('Short bio about yourself'),
                                            'rows':4, 'cols':15, 'required': False}),
    'user_occupation'    : forms.TextInput(attrs={'placeholder':_('Your occupation'), 'required': False}),
    'user_nationality'    : forms.TextInput(attrs={'placeholder':_('Your Nationality'), 'required': False}),
}

user_extra_fields = ['user_first_name', 'user_last_name', 'user_dob','user_gender','user_github', 'user_linkedin', 'user_bio', 'user_occupation', 'user_nationality' ]

user_fields = [ 'email', 'username' ]

captcha_attrs = {'theme': 'clean', 'size': 'compact'}


class UserRegistrationForm(ModelForm):
    repass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re Enter Password',
                                                     'min_length':1, 'max_length':20}))

    class Meta:
        model = User
        fields = user_fields + ['password']
        widgets = user_widgets
        widgets['password'] = forms.PasswordInput(attrs={'placeholder':_('Password')})


    def clean(self):
        password, re_password = self.cleaned_data.get('password'), self.cleaned_data.get('repass')
        if password and password != re_password:
            raise forms.ValidationError(_("Passwords don\'t match"))
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Email "%s" is already in use.') % email)
        return email


    def clean_repass(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repass')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don\'t match"))
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user



course_fields = ['course_name', 'course_bio', 'course_language', 'course_difficulty',
                  'course_fees']
course_widgets = {
    'course_name'    : forms.TextInput(attrs={'placeholder':_('Course Name'), 'required': True}),
    'course_bio'    :  CKEditorWidget(),
    'course_fees' : forms.TextInput(attrs={'placeholder':_('Course fees'), 'required': True}),
}

class CourseRegistrationForm(ModelForm):
    class Meta:
        model = Course
        fields = course_fields
        widgets = course_widgets
        exclude = ['course_user']


course_module_fields = ['module_name', 'module_description', 'module_duration']
course_module_widgets = {
    'module_name'    : forms.TextInput(attrs={'placeholder':_('Module Name'), 'required': True}),
    'module_description'    :  CKEditorWidget(),
    'module_duration' : forms.TextInput(attrs={'placeholder':_('Duration of module'), 'required': True}),
}


class ModuleAddForm(ModelForm):
    class Meta:
        model = CourseModules
        fields = course_module_fields
        widgets = course_module_widgets
        exclude = ['course']



solution_fields = ['solution_name', 'solution_platform','solution_contact_email', 'solution_contact_phone','solution_deadline','solution_budget','solution_description']
solution_widgets = {
    'solution_name'    : forms.TextInput(attrs={'placeholder':_('Solution Name'), 'required': True}),
    'solution_contact_email'    :  forms.TextInput(attrs={'placeholder':_('Contact Email'),
                                             'required': True}),
    'solution_contact_phone' : forms.TextInput(attrs={'placeholder':_('Contact Number'), 'required': False}),
    'solution_deadline' : DateTimePicker(options={"getUTCDate": True, "pickTime": True,
                                              "date":"fa fa-calendar", "viewMode":'years',
                                              "format":'DD/MM/YYYY'},
                                     attrs={'placeholder':_('DD/MM/YYYY'), 'required': True, 'class':'datepicker'}),
    'solution_budget' : forms.TextInput(attrs={'placeholder':_('Expected Budget ( in INR )'), 'required': True}),
    'solution_description'    :  forms.Textarea(attrs={'placeholder':_('Solution Description'),
                                            'rows':4, 'cols':15, 'required': True}),
}

class SolutionCreateForm(ModelForm):

    class Meta:
        model = Solution
        fields = solution_fields
        widgets = solution_widgets


progress_fields = ['completed','remarks']

class ProgressForm(ModelForm):

    class Meta:
        fields = progress_fields
        model = CourseProgress
