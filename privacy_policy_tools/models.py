
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
This module provides the models of the privacy_policy_tools.
"""
import random
import string

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class PrivacyPolicy(models.Model):
    """
    This model saves different versions of privacy policies which have to
    be accepted by the user.

    Fields:
        - title -- title of the policy
        - text -- text of the policy
        - active -- true if the policy is active
        - published_at -- date of publishing
        - for_group -- user group
    """
    title = models.CharField(max_length=128, verbose_name=_('Title'),
                             default=_('Privacy Policy'))
    text = HTMLField(verbose_name=_('Text'))
    confirm_checkbox = models.BooleanField(
        default=False, verbose_name=_('Confirm checkbox'))
    confirm_checkbox_text = models.CharField(
        max_length=128, verbose_name=_('Confirm checkbox text'))
    confirm_button_text = models.CharField(
        max_length=128, verbose_name=_('Confirm button text'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    published_at = models.DateTimeField(default=timezone.now,
                                        verbose_name=_('Published at'))
    for_group = models.ForeignKey(Group, on_delete=models.CASCADE,
                                  blank=True, null=True,
                                  verbose_name=_('For group'))

    def __str__(self):
        """
        Unicode representation
        """
        return _('Privacy Policy') + ': ' + str(self.published_at)

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policies')


class PrivacyPolicyConfirmation(models.Model):
    """
    This model saves when a user confirmed a Privacy
    Policy.

    Fields:
        - user -- confirming user
        - confirmed_at -- date and time of confirmation
        - privacy_policy -- the confirmed privacy policy
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name=_('User'))
    confirmed_at = models.DateTimeField(default=timezone.now,
                                        verbose_name=_('Confirmed at'))
    privacy_policy = models.ForeignKey(PrivacyPolicy,
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Privacy Policy'))
    second_confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Second confirmed at'),
        default=None
    )

    def __str__(self):
        """
        Unicode Representation
        """
        return _('Confirmed at') + ': ' + str(self.confirmed_at)

    class Meta:
        verbose_name = _('Privacy Policy Confirmation')
        verbose_name_plural = _('Privacy Policy Confirmations')


class OneTimeToken(models.Model):
    """
    This model represents a token for second confirmation.

    Fields:
        - token -- token to use
        - created_at -- datetime of token creation
        - confirmation -- confirmation to which the token is related
    """
    LENGTH = 32
    token = models.CharField(
        max_length=LENGTH,
        verbose_name=_('Token')
    )
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name=_('Created at'))
    confirmation = models.ForeignKey(PrivacyPolicyConfirmation,
                                     on_delete=models.CASCADE,
                                     verbose_name=_('Confirmation'))

    def __str__(self):
        """
        Unicode Representation
        """
        return str(self.token)

    @classmethod
    def create_token(cls, confirmation):
        """
        Creates a new token.

        Args:
            confirmation: confirmation for the token

        Returns:
            the created token
        """
        token = cls._generat_token()
        while cls.objects.filter(token=token,
                                 confirmation=confirmation).exists():
            token = cls._generat_token()
        ott = cls(token=token, confirmation=confirmation)
        ott.save()
        return ott

    @classmethod
    def _generat_token(cls):
        """
        Generates a new token string.

        Returns:
            the token string
        """
        token = ''.join(
            random.choice(string.ascii_lowercase) for i in range(
                0, cls.LENGTH))
        return token

    class Meta:
        verbose_name = _('One Time Token')
        verbose_name_plural = _('One Time Tokens')
