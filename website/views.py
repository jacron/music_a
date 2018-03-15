# from PIL import ImageGrab
import json
from channels import Group
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

folderpath = '/Volumes/Media/tmp/folder.jpg'


def socket_log(msg, mode, id=None):
    Group("chat").send({
        "text": json.dumps({
            'msg' : msg,
            'mode': mode,
            'id': id
        })
    })


def hello(request):
    # img = ImageGrab.grabclipboard()
    # if img:
    #     img.save(folderpath)
    # else:
    #     print('no image on clipboard!')
    socket_log('testing socket', 'info')
    template = loader.get_template('website/hello.html')

    return HttpResponse(template.render({}, request))