from django.http import HttpResponse
from django.template import loader
from website.db.fetch import get_tags, get_tag, get_tag_albums
from website.db.update import delete_tag


def tag_view(request, tag_id):
    template = loader.get_template('website/tag.html')
    return HttpResponse(template.render(
    {
        'items': get_tag_albums(tag_id),
        "tag": get_tag(tag_id)
    }, request))


def tag_delete(request, tag_id):
    tag = get_tag(tag_id)
    delete_tag(tag_id)
    template = loader.get_template('website/tag_deleted.html')
    return HttpResponse(template.render(
    {
        "tag": tag
    }, request))


def tag(request, tag_id):
    return tag_view(request, tag_id)


def tags(request):
    template = loader.get_template('website/tags.html')
    return HttpResponse(template.render(
        {
            "tags": get_tags(),
        }, request))
