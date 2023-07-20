from django.shortcuts import render, reverse
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect

class NewTaskForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={'class': 'larger-textarea'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(), 
        "text": markdown2.markdown(util.get_entry(entry))
    })

def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'encyclopedia/add.html', {
                'form': form
            })
    return render(request, 'encyclopedia/add.html', {
        'form': NewTaskForm()
    })