from django.shortcuts import render
import random
import markdown2
from . import util

# open the home page with a list of entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#  opens a specific entry
def entrypage(request, entryname):
    entry =util.get_entry(entryname)
    if entry:
        return render(request, "encyclopedia/entrypage.html", {
            "entry": markdown2.markdown(entry),
            "entryname": entryname
        })
    else:
        return render(request, "encyclopedia/entrypage.html", {
            "entry": entry,
            "entryname": entryname
        })

# get and render a random entry page
def randomEntry(request):
    # get a random entry name the all the list of entries
    entryname = random.choice(util.list_entries())
    return render(request, "encyclopedia/entrypage.html", {
        "entry": markdown2.markdown(util.get_entry(entryname)),
        "entryname": entryname
    })


# edit a specific entry
def editEntry(request, entryname):
    # // save edited entry page
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(entryname, content)
        return render(request, "encyclopedia/entrypage.html", {
            "entry": markdown2.markdown(util.get_entry(entryname)),
            "entryname": entryname
            })

    # open page for editing entry content
    return render(request, "encyclopedia/editEntry.html", {
        "entry": util.get_entry(entryname),
        "entryname": entryname
    })

# create an entry
def createEntry(request):
    if request.method =="POST":
        # get title and content of entry page
        title = request.POST['title']
        content = request.POST['content']
        entry = util.get_entry(title)
        # render page with error if title exist
        if entry:
            return render(request, "encyclopedia/createEntry.html", {
                "Error": "Title of entry page already exist",
                "content": content
            })
        else: 
            # save entry
            if title:
                util.save_entry(title, content)
                return render(request, "encyclopedia/createEntry.html")
            else:
                # render page with error if no title is entered
                return render(request, "encyclopedia/createEntry.html", {
                    "Error": "Title of entry page cannot be empty",
                    "content": content
                    })
    return render(request, "encyclopedia/createEntry.html")

def searchEntry(request):
    if request.method == "GET":
        # get the searched entry page name
        if request.GET['q']:
            entryname = request.GET['q']
            result = util.get_entry(entryname)
            # render page if entry name exist
            if result:
                 return render(request, "encyclopedia/entrypage.html", {
                    "entry": markdown2.markdown(result),
                    "entryname": entryname
                    })
            else:
                # search for entry page name that contains the search keyword
                entryList = util.list_entries()
                matchedEntries = []
                for entry in entryList:
                    if entryname.lower() in entry.lower():
                        matchedEntries.append(entry)
                # render the page with a list of entry page titles that contain the search
                # keyword
                return render(request, "encyclopedia/index.html", {
                    "entries": matchedEntries
                    })
        # render an error page if search box is empty
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "Error": "No search keyword provided"
            })
    # render home page if another method of request is used
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })