
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
This module provides some helper functions of the privacy_policy_tools.
"""

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404
from django.utils import timezone

from privacy_policy_tools.models import PrivacyPolicy, \
    PrivacyPolicyConfirmation


def get_by_py_path(py_path):
    """
    Imports and returns a python callable.

    Keyword arguments:
        py_path -- callable to load
    """
    parts = py_path.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_active_policies():
    """
    Returns a list of active policies.
    """
    policies = []
    try:
        nogroup = PrivacyPolicy.objects.filter(
            for_group=None, active=True).order_by('-published_at')
        policies.extend(nogroup)
    except PrivacyPolicy.DoesNotExist:
        pass
    groups = Group.objects.all().order_by('name')
    for group in groups:
        try:
            active = group.privacypolicy_set.filter(
                active=True).order_by('-published_at')
            policies.extend(active)
        except PrivacyPolicy.DoesNotExist:
            pass
    return policies


def get_active_policies_for_group(group=None):
    """
    Returns a list of active policies.
    """
    if group is None:
        try:
            nogroup = PrivacyPolicy.objects.filter(
                for_group=None, active=True).order_by('-published_at')
            return nogroup
        except PrivacyPolicy.DoesNotExist:
            return []
    else:
        try:
            active = group.privacypolicy_set.filter(
                active=True).order_by('-published_at')
            return active
        except PrivacyPolicy.DoesNotExist:
            return []


def get_setting(key, default=None):
    """
    Returns a settings value.

    Keyword arguments:
        - key -- name of the settings value
        - default -- default value
    """
    try:
        return settings.PRIVACY_POLICY_TOOLS.get(key, default)
    except AttributeError:
        return None
    except KeyError:
        return None


def save_confirmation(user):
    """
    Saves a confirmation to policies according to the given user.

    Keyword arguments:
        - user -- user object
    """
    policies = get_active_policies()
    if len(policies) <= 0:
        raise Http404
    for policy in policies:
        if get_setting('DEFAULT_POLICY', True):
            no = policy.for_group is None
        else:
            no = policy.for_group is None \
                and len(user.groups.all()) <= 0
        if policy.for_group in user.groups.all() or no:
            confirms = PrivacyPolicyConfirmation.objects.filter(
                privacy_policy=policy, user=user)
            if len(confirms) <= 0:
                confirmation = PrivacyPolicyConfirmation(
                    user=user,
                    confirmed_at=timezone.now(),
                    privacy_policy=policy)
                confirmation.save()
