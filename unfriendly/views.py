from urllib import unquote
from urlparse import urlparse

from django.core.urlresolvers import resolve, Resolver404
from django.http import HttpResponseNotFound

from unfriendly import settings
from unfriendly.utils import decrypt, CheckSumError


def deobfuscate(request, key, juice=None):
    """
    Deobfuscates the URL and returns HttpResponse from source view.
    SEO juice is mostly ignored as it is intended for display purposes only.
    """
    try:
        url = decrypt(str(key),
                      settings.UNFRIENDLY_SECRET,
                      checksum=settings.UNFRIENDLY_ENFORCE_CHECKSUM)
    except CheckSumError:
        return HttpResponseNotFound()

    url_parts = urlparse(unquote(url))
    path = url_parts.path
    query = url_parts.query

    try:
        view, args, kwargs = resolve(path)
    except Resolver404:
        return HttpResponseNotFound()

    # fix-up the environ object
    environ = request.environ.copy()
    environ['PATH_INFO'] = path[len(environ['SCRIPT_NAME']):]
    environ['QUERY_STRING'] = query

    # init a new request
    session = request.session
    patched_request = request.__class__(environ)
    patched_request.session = session

    response = view(patched_request, *args, **kwargs)

    # offer up a friendlier juice-powered filename if downloaded
    if juice and not response.has_header('Content-Disposition'):
        response['Content-Disposition'] = 'inline; filename=%s' % juice

    return response
