# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import static

import l10n_utils


def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if not getattr(settings, 'DEBUG', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def server_error_view(request, template_name='500.html'):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, status=500)


def static_serve(request, path, document_root):
    """Serve static files under /media/"""
    css_match = re.match(r'^css/l10n/([a-z]+(?:-[A-Z]+)?)/intl\.css$', path)

    # If the requested URL is a locale-specific CSS and it doesn't exist,
    # serve a blank CSS file instead of a generic 404 Not Found error
    if (css_match and css_match.group(1) in settings.PROD_LANGUAGES
            and not os.path.exists(os.path.join(document_root, path))):
        return HttpResponse('', content_type='text/css')

    # Serve a static file as usual
    return static.serve(request, path, document_root)
