from django.http import HttpResponse
from django.template import loader
from website.db.fetch import get_gatherers


def gather(request):
    template = loader.get_template('website/gatherers.html')
    return HttpResponse(template.render(
        {
            "albums": get_gatherers()
        }, request))


