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
This module designs the urls of the package privacy_policy_tools.
"""

from django.urls import re_path
from privacy_policy_tools.utils import get_setting
from privacy_policy_tools.views import confirm, show, \
    second_confirm_required, second_confirm

confirm_url = get_setting('POLICY_CONFIRM_URL')
page_url = get_setting('POLICY_PAGE_URL')
second_confirm_required_url = get_setting('SECOND_CONFIRM_REQUIRED_URL',
                                          'confirm/second/required')
second_confirm_url = get_setting('SECOND_CONFIRM_URL',
                                 'confirm/second')

urlpatterns = [
    re_path(r'^' + page_url + r'$',
            show, name='privacy_policy_tools.views.show'),
    re_path(r'^' + confirm_url + r'/(?P<policy_id>[0-9]+)$',
            confirm, name='privacy_policy_tools.views.confirm'),
    re_path(r'^' + confirm_url + r'/(?P<policy_id>[0-9]+)/next(?P<next>.+)$',
            confirm, name='privacy_policy_tools.views.confirm'),
    re_path(r'^' + second_confirm_required_url + r'/(?P<confirm_id>[0-9]+)$',
            second_confirm_required,
            name='privacy_policy_tools.views.second_confirm_required'),
    re_path(r'^' + second_confirm_url + r'/(?P<confirm_id>[0-9]+)/next('
                                        r'?P<token>[a-z]+)$',
            second_confirm, name='privacy_policy_tools.views.second_confirm'),
]
