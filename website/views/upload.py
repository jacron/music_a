from django.http import HttpResponse
from django.template import loader


def uploadalbum(request):
    template = loader.get_template('website/upload.html')
    return HttpResponse(template.render(
        {
        }, request
    ))