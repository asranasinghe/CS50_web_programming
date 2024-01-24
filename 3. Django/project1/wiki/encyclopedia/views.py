from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_md = util.get_entry(title)

    if entry_md is None:
        content = 'Page Does Not Exist'

    else:
        content = Markdown().convert(entry_md)
        
    return render(request, "encyclopedia/entry.html", {
        "content": content
    })

