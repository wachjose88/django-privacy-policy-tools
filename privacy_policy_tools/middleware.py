
# Copyright (c) 2022-2023 Josef Wachtler
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
This module provides some middleware for the package privacy_policy_tools.
"""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from privacy_policy_tools.utils import get_setting, get_active_policies, \
    get_by_py_path
from privacy_policy_tools.models import PrivacyPolicyConfirmation


class PrivacyPolicyMiddleware(object):
    """
    This middleware class forces the user to confirm the privacy policies.
    """

    def __init__(self, get_response):
        """
        constructor: sets get_response
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes the request and redirect to the privacy policy if
        the user has not confirmed it yet.

        Keyword arguments:
            - request -- calling HttpRequest
        """
        response = self.get_response(request)
        enabled = get_setting('ENABLED')
        if enabled is None:
            return response
        if enabled is True:
            url = get_setting(
                'POLICY_PAGE_URL',
                'terms/and/conditions'
            )
            ignore_urls = get_setting(
                'IGNORE_URLS',
                []
            )
            if request.user.is_authenticated and \
                    url not in request.path_info and \
                    all(ignore not in request.path_info
                        for ignore in ignore_urls):
                start_hook = get_setting('START_HOOK', None)
                if start_hook is not None:
                    start_hook = get_by_py_path(start_hook)
                    if start_hook(request) is False:
                        return response
                policies = get_active_policies()
                if len(policies) <= 0:
                    return response
                for policy in policies:
                    if get_setting('DEFAULT_POLICY', True):
                        no = policy.for_group is None
                    else:
                        no = policy.for_group is None \
                            and len(request.user.groups.all()) <= 0
                    if policy.for_group in request.user.groups.all() or no:
                        confirms = PrivacyPolicyConfirmation.objects.filter(
                            privacy_policy=policy, user=request.user)
                        if len(confirms) <= 0:
                            next_view = self._generate_next(request)
                            return HttpResponseRedirect(reverse(
                                'privacy_policy_tools.views.confirm',
                                args=(policy.id, next_view,)))
                        else:
                            second = self._second_confirmation(
                                request, confirms.first())
                            if second is not None:
                                return second
        return response

    def _second_confirmation(self, request, confirmation):
        required_hook = get_setting('SECOND_CONFIRMATION_REQUIRED_HOOK',
                                    None)
        if required_hook is None:
            return None
        if required_hook is not None:
            required_hook = get_by_py_path(required_hook)
            if required_hook(request, confirmation) is False:
                return None
        if confirmation.second_confirmed_at is not None:
            return None
        return HttpResponseRedirect(reverse(
            'privacy_policy_tools.views.second_confirm_required',
            args=(confirmation.id, )
        ))

    def _generate_next(self, request):
        next_view = request.path_info
        login_view = reverse('login')
        if next_view == login_view:
            next_view = request.POST.get(
                'next',
                request.GET.get(
                    'next',
                    settings.LOGIN_REDIRECT_URL
                )
            )
            if not url_has_allowed_host_and_scheme(
                    next_view,
                    {request.get_host(), *set(
                        settings.ALLOWED_HOSTS
                    )},
                    request.is_secure()
            ):
                next_view = settings.LOGIN_REDIRECT_URL
        return next_view
