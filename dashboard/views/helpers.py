from pyramid.httpexceptions import HTTPBadRequest


def check_post_csrf(func):
    """
    Verify the csrf_token only if the request method is POST

    Useful when you gave the same view function handling both POST and GET
    requests
    :param func: the decorated view function
    :return: the new callable that decorates the view
    """
    def inner(context, request):
        if request.method == "POST":
            if request.session.get_csrf_token()\
                    != request.POST.get('csrf_token'):
                return HTTPBadRequest("Bad csrf token")
        # fall through if not POST or token is valid
        return func.__call__(context, request)
    return inner