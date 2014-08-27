__author__ = 'xxd'

from django.shortcuts import render_to_response
from django.template import RequestContext

def server_error(request):
    """
    500 error handler.
    Templates: `500.html`
    Context: None
    """
    return render_to_response('500.html',
        RequestContext(request)
    )
