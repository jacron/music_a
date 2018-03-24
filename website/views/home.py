# from channels import Group
import json

from django.http import HttpResponse
from django.template import loader

from website.views.ajax import upload
from website.views.ajaxget import do_get
from website.views.ajaxpost import do_post


def home(request):
    template = loader.get_template('website/home.html')
    return HttpResponse(template.render(
        {
        }, request))


def ajax(request):
    msg = 'No post, files or get!'
    msg = json.dumps(msg)
    if request.POST:
        msg = do_post(request.POST)
        msg = json.dumps(msg)
    if request.GET:
        msg = do_get(request.GET)
    if request.FILES:
        msg = upload(request.POST, request.FILES)
    return HttpResponse(msg)
