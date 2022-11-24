import random
import markdown2

from django.shortcuts import render, redirect

from . import util
from markdown2 import Markdown

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": f"{title} does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
        entry_search = request.GET.get('q','')
        if(util.get_entry(entry_search) is not None):
            return redirect('entry', title=entry_search)
        else:
            recommendation = []
            for entry in util.list_entries():
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": recommendation,
                "search": True,
                "title": entry_search
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"{title} page already exists."
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return redirect('entry', title=title)


def edit(request, edit_name):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title=title)

def random_page(request):
    rand_entry_name = random.choice(util.list_entries())
    return redirect('entry', title=rand_entry_name)