
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

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from privacy_policy_tools.models import PrivacyPolicy, \
    PrivacyPolicyConfirmation
from privacy_policy_tools.utils import get_active_policies


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
        confirmation = PrivacyPolicyConfirmation(
            user=request.user,
            confirmed_at=timezone.now(),
            privacy_policy=policy)
        confirmation.save()
        return HttpResponseRedirect(next)

    params = {
        'policy': policy,
        'is_confirmed': is_confirmed,
        'is_authenticated': request.user.is_authenticated,
        'form_url': url
    }

    return render(
        request, 'privacy_policy_tools/confirm.html', params)
