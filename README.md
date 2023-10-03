# Django Privacy Policy Tools

This is a Django app to manage privacy policies and to handle the
process of confirmation trough the users. 

Features: 

* Create policies using the admin interface
* Different policies for different groups
* Text styling with html
* Confirmation middleware to force the users to confirm the policies
* View all confirmations in the admin interface

This app is build for the current LTS Version of 
[Django](https://www.djangoproject.com/), which is 4.2.

## Install

Install the app using pip.

```shell
pip install django-privacy-policy-tools
```

## Configure

At first you have to add the app to your `INSTALLED_APPS` in your `settings.py`.

```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'privacy_policy_tools.apps.PrivacyPolicyToolsConfig',
    ...
)
```

Add the middleware of the app to your `MIDDLEWARE` in your `settings.py`.

```python
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'privacy_policy_tools.middleware.PrivacyPolicyMiddleware',
    ...
)
```

Add the URL configuration to your main urls.py:

```python
urlpatterns = [
    ...
    re_path(r'^privacy/', include('privacy_policy_tools.urls')),
    ...
]
```

If you want to use the app in your templates (e.g. create a link to 
the privacy policy page), you should 
add the context processor of the app to your config in your `settings.py`.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'privacy_policy_tools.context_processors.privacy_tools',
            ],
            'debug': True,
        },
    },
]
```

Now you can configure the app in your `settings.py`.

```python
PRIVACY_POLICY_TOOLS = {
    'ENABLED': True,
    'POLICY_PAGE_URL': 'terms/and/conditions',
    'POLICY_CONFIRM_URL': 'terms/and/conditions/confirm',
    'IGNORE_URLS': ['admin', ],
    'DEFAULT_POLICY': True
}
```

Possible values are: 

* __ENABLED__: True to enable the privacy policy tools. This means the users
  have to confirm the created policies.
* __POLICY_PAGE_URL__: URL schema of the policy page to show all active policies
* __POLICY_CONFIRM_URL__: URL schema of the page to confirm a policy
* __IGNORE_URLS__: List of URLs which contains these values could be accessed without
  confirming a policy. Add the admin site to let you create a policy.
* __DEFAULT_POLICY__: If true the policy created for no group has to be confirmed
  by all users. If false such a policy has to be confirmed by users with no group only. 

## Usage

After configuring the app everything is ready to be used. Start by creating a policy
in the admin interface. It is possible to create different policies for different groups.
Depending on your language settings you will get a field for each language for the policy
title and text.

Now the users are required to confirm your created policies.

## Customization

### Overwrite templates to customize the style

The included templates are using the base templet of the admin site. If you want
to change this style to match your project you can overwrite these two templates
by placing them in an app loaded in `INSTALLED_APPS` before this app. There
are the following templates:

* `privacy_policy_tools/show.html`
* `privacy_policy_tools/confirm.html`

In `show.html` you have to place something like this: 

```
{% for policy in policies %}
    <h3>{{ policy.title }}</h3>
    <p><small>{% translate "Last changed:" %} {{ policy.published_at }}</small></p>
    <p>{{ policy.text|safe }}</p>
{% endfor %}
```

In `confirm.html` you have to do something like this: 

```
<h3>{{ policy.title }}</h3>
<p>{% translate "Last changed:" %}
    {{ policy.published_at }}</p>

<p>{{ policy.text|safe }}</p>

{% if is_authenticated and not is_confirmed %}
    {% if policy.confirm_checkbox is True %}
        {% if form.non_field_errors %}
        <ul class="errorlist">
            <li>{{ form.non_field_errors }}</li>
        </ul>
        {% endif %}
    {% endif %}
    <form method="post" action="{{ form_url }}">
        {% csrf_token %}
        {% if policy.confirm_checkbox is True %}
            {% for field in form %}
            {% if field.errors %}
            <ul class="errorlist">
                {% for error in field.errors %}
                <li>{{ error|escape }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            <div class="checkbox">
                {{ field }} {{ field.label }}
            </div>
            {% endfor %}
        {% endif %}
        <input type="submit" class="default" id="btn_create"
               value="{{ policy.confirm_button_text }}"
            style="float: left !important;"/>
    </form>
{% endif %}
```

### Link to policies

If you want to place a link to the policies at your page (e.g. in the footer)
you have to add a context processor as shown above. After that you can
create the link in your template in the following way:

```
{% if privacy_enabled %}
    <a href="{% url privacy_view %}">{% translate "Terms and Conditions" %}</a>
{% endif %}
```

### Add confirm checkbox to your registration form

To add a checkbox to your registration form where the users could confirm
your policies during registration, you have to do multiple things. At first
create the form and add the fields: 

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from privacy_policy_tools.utils import get_setting

class UserCreateForm(UserCreationForm):
  
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        if get_setting('ENABLED', False):
            self.fields['confirm_privacy'] = forms.BooleanField(
                label=_('I accept the Terms and Conditions')
            )
```

In the corresponding view you have to save the confirmation. Such a view
could look like this: 

```python
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from privacy_policy_tools.utils import save_confirmation, get_setting
from yourapp.forms import UserCreateForm

def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, label_suffix='')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            if get_setting('ENABLED'):
                save_confirmation(user)
            return HttpResponseRedirect(reverse('yourapp.views.index'))

    else:
        form = UserCreateForm()

    return render(request, 'registration/create_user.html', {
        'form': form,
    })
```

### Start hook

It is possible to add a hook at the beginning of the evaluation if the
privacy policy should be shown to the user. With this hook you can perform
additional checks depending on your project.

To add this hook add the following setting to the configuration in `settings.py`:

* __START_HOOK__: a function in python-dotted syntax to check if the policy
 should be displayed. The function takes one argument which is the Django request
 object. It should return True if the policy should be displayed or False if not.

## Second confirmation

The app is able to request a second confirmation to a privacy policy. This may be 
case if a confirmation of a parent is required. For that an email is sent to the
person for the second confirmation.

To use this feature some settings must be provided:

* __SECOND_CONFIRMATION_REQUIRED_HOOK__: a function in python-dotted syntax to
 decide if a second confirmation is required. It takes the Django request object
 as the first parameter. The second parameter is the confirmation object of this
 app for which a second confirmation is required. It should return True if a 
 second confirmation is required or False if not.
* __SECOND_CONFIRMATION_SAVE_EMAIL_HOOK__: a function in python-dotted syntax to
 save the entered email to which the request for the second confirmation will be 
 sent. The first parameter is the Django request object and the second one is the
 email. There is no return value.
* __SECOND_CONFIRMATION_GET_EMAIL_HOOK__: a function in python-dotted syntax to
 get the saved email for the second confirmation. The only parameter is the Django
 request object. It should return the email as a string or None if there is no
 email.
* __SECOND_CONFIRM_VALID_FOR_MINUTES__: optionally provide the timespan for how
 long the second confirmation link should be valid. It has to be an integer 
 providing the time in minutes. Default is 10.

To further customize the templates it is possible to override them. For that copy
the templates beginning with second_confirm to your project and change it
according to your needs.
