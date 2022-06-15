
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
This module provides the admin settings of the privacy_policy_tools.
"""

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from privacy_policy_tools.models import PrivacyPolicy, \
    PrivacyPolicyConfirmation


class PrivacyPolicyConfirmationInline(admin.TabularInline):
    """
    This admin inline handles the Privacy Policy Confirmations.
    """
    model = PrivacyPolicyConfirmation
    fields = ('user', 'privacy_policy', 'confirmed_at', )
    extra = 0


class PrivacyPolicyAdmin(TranslationAdmin):
    """
    Creating and editing Privacy Policies. The confirmations
    are shown inline.
    """
    list_display = ('title', 'published_at', 'for_group', 'active')
    list_filter = ['published_at', 'active']
    search_fields = ['title', 'text']
    date_hierarchy = 'published_at'

    inlines = [PrivacyPolicyConfirmationInline]


admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
