
# Copyright (c) 2022 Josef Wachtler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides the views of the privacy_policy_tools.
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from privacy_policy_tools.models import PrivacyPolicy, \
    PrivacyPolicyConfirmation
from privacy_policy_tools.utils import get_active_policies, get_setting, \
    get_by_py_path
from privacy_policy_tools.forms import ConfirmForm, SecondConfirmGetEmail


def show(request):
    """
    Displays the Privacy Policies.

    Keyword arguments:
        - request -- the calling HttpRequest

    Template: privacy_policy_tools/show.html
    """
    policies = get_active_policies()
    params = {
        'policies': policies
    }

    return render(
        request, 'privacy_policy_tools/show.html', params)


def confirm(request, policy_id, next='/terms/and/conditions'):
    """
    Displays the Privacy Policy and asks for confirmation.

    Keyword arguments:
        - request -- the calling HttpRequest
        - next -- path to redirect after confirmation

    Template: privacy_policy_tools/confirm.html
    """
    policy = get_object_or_404(PrivacyPolicy, id=policy_id)

    url = reverse('privacy_policy_tools.views.confirm',
                  args=(policy_id,))

    is_confirmed = False
    if request.user.is_authenticated:
        confirmations = PrivacyPolicyConfirmation.objects.filter(
            privacy_policy=policy, user=request.user)
        if len(confirmations) > 0:
            is_confirmed = True
        else:
            url = reverse('privacy_policy_tools.views.confirm',
                          args=(policy_id, next,))

    if request.method == 'POST' and not is_confirmed \
            and request.user.is_authenticated:
        if policy.confirm_checkbox is True:
            form = ConfirmForm(
                request.POST,
                agree_label=policy.confirm_checkbox_text)
            if form.is_valid():
                confirmation = PrivacyPolicyConfirmation(
                    user=request.user,
                    confirmed_at=timezone.now(),
                    privacy_policy=policy)
                confirmation.save()
                return HttpResponseRedirect(next)
        else:
            confirmation = PrivacyPolicyConfirmation(
                user=request.user,
                confirmed_at=timezone.now(),
                privacy_policy=policy)
            confirmation.save()
            return HttpResponseRedirect(next)
    else:
        if policy.confirm_checkbox is True:
            form = ConfirmForm(agree_label=policy.confirm_checkbox_text)

    params = {
        'policy': policy,
        'is_confirmed': is_confirmed,
        'is_authenticated': request.user.is_authenticated,
        'form_url': url
    }
    if policy.confirm_checkbox is True:
        params['form'] = form

    return render(
        request, 'privacy_policy_tools/confirm.html', params)


@login_required
def second_confirm_required(request, confirm_id):
    confirmation = get_object_or_404(PrivacyPolicyConfirmation,
                                     id=confirm_id)
    if confirmation.second_confirmed_at is not None:
        raise Http404
    get_hook = get_setting(
        'SECOND_CONFIRMATION_GET_EMAIL_HOOK', None)

    if get_hook is not None:
        get_hook = get_by_py_path(get_hook)
        parent_email = get_hook(request)
    else:
        raise Http404

    url = reverse('privacy_policy_tools.views.second_confirm_required',
                  args=(confirmation.id, ))
    if request.method == 'POST':
        form = SecondConfirmGetEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            save_hook = get_setting(
                'SECOND_CONFIRMATION_SAVE_EMAIL_HOOK', None)

            if save_hook is not None:
                save_hook = get_by_py_path(save_hook)
                save_hook(request, email)
            else:
                raise Http404
            return HttpResponseRedirect('/')
    else:
        if parent_email is not None:
            data = {'email': parent_email}
            form = SecondConfirmGetEmail(initial=data)
        else:
            form = SecondConfirmGetEmail()
    params = {
        'form': form,
        'policy': confirmation.privacy_policy,
        'confirmation': confirmation,
        'form_url': url,
        'parent_email': parent_email
    }

    return render(
        request,
        'privacy_policy_tools/second_confirm_required.html',
        params)
