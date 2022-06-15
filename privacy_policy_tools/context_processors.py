
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
This module provides some context processors.
"""

from privacy_policy_tools.utils import get_setting


def privacy_tools(request):
    """
    Adds some values to the templates.

    Values:
        - privacy_enabled -- true if the privacy policy tools are enabled
        - privacy_view -- name of the view to show the policies

    Keyword arguments:
        - request -- the calling HttpRequest
    """
    enabled = get_setting(
        'ENABLED',
        'terms/and/conditions'
    )
    v = {
        'privacy_enabled': enabled,
        'privacy_view': 'privacy_policy_tools.views.show'
    }

    return v
