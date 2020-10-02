from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from random import choice
import re
from . import util
from markdown2 import Markdown


class searchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search'}))


class addNewEntry(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 50,
                                  'cols': 40,
                                  'style': 'height: 25em;' }))


def index(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            entries = util.list_entries()
            rgx = re.compile(f'^{search}+', re.IGNORECASE)
            ls = [rs for rs in entries if rgx.match(rs)]
            if len(ls) == 1 and search.lower() == ls[0].lower():
                return HttpResponseRedirect(reverse('ency:entry', args=[search]))
            else:
                return render(request, "encyclopedia/resultsPage.html", {
                    "entries": ls,
                    "form": searchForm()
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": searchForm()
        })


def entry(request, entry):
    if entry == "random":
        entries = util.list_entries()
        random_entry = choice(entries)
        return HttpResponseRedirect(reverse('ency:entry', args=[random_entry]))
    elif request.method == 'POST':
        form = addNewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.update_entry(title, content)
            return HttpResponseRedirect(reverse('ency:entry', args=[entry]))
    else:
        newEntry = util.get_entry(entry)
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(newEntry),
            "title": f"{entry}"
        })


def newPage(request):
    if request.method == 'POST':
        form = addNewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entry = util.save_entry(title, content)
            if entry == "ERROR":
                return HttpResponse("ERROR File already exist")
            else:
                return HttpResponseRedirect(reverse('ency:entry', args=[title]))
    else:
        return render(request, "encyclopedia/newPage.html", {
            "newEntry": addNewEntry()
        } )


def updatePage(request, title):
    content = util.get_entry(title)
    initial = {'title':f"{title}", 'content': f"{content}"}
    form = addNewEntry(initial=initial)
    return render(request, 'encyclopedia/updatePage.html', {
        'title': f"{title}",
        'update_form': form

    })
    
