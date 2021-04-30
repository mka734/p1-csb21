from django.http import QueryDict
from .models import Log, User


# Vulnerability (sensitive POST params may be logged)
def LoggingMiddleware(get_response):
    def middleware(request):
        response = get_response(request)

        if request.POST is None or len(QueryDict.urlencode(request.POST)) == 0:
            return response

        post = QueryDict.copy(request.POST)
        if 'password' in request.POST:
            post.pop('password')
        if 'csrfmiddlewaretoken' in request.POST:
            post.pop('csrfmiddlewaretoken')

        path = request.get_full_path()
        params = QueryDict.urlencode(post)
        remote_addr = request.META['REMOTE_ADDR']
        user = None

        try:
            user = User.objects.get(id=request.user.id)
        except:
            user = None

        log = Log(path=path, params=params, remote_addr=remote_addr,
                  user=user)
        log.save()

        return response
    return middleware
