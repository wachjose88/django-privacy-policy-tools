
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
This module provides the forms of the privacy_policy_tools.
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class SecondConfirmGetEmail(forms.Form):
    use_required_attribute = False
    email = forms.EmailField(
        label=_('E-mail'),
        required=True
    )


class ConfirmForm(forms.Form):
    """
    This is a form to confirm a policy

    Fields:
        - agree -- true to agree to a policy
    """
    use_required_attribute = False
    agree = forms.BooleanField(required=True)

    def __init__(self, *args, **kwrds):
        """
        constructor
        sets label
        """
        agree_label = kwrds.pop('agree_label')
        super(ConfirmForm, self).__init__(*args, **kwrds)
        self.fields['agree'].label = _(agree_label)
