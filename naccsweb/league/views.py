from django.shortcuts import render

from .forms import SchoolSearchForm
from .models import School

# Create your views here.
def school_search(request):
    if (request.method == "POST"):
        form = SchoolSearchForm(request.POST)

        if (form.is_valid()):
            search_results = watson.filter(School, form.data['query'])
            return render(request, 'school/search.html', {'form': form, 'results':search_results})
    else:
        form = SchoolSearchForm()
    
    return render(request, 'school/search.html', {'form': form})

def school(request, school_id):
    return render(request, 'school/school.html')

def hub(request):
    return render(request, 'hub.html')

def league(request):
    return render(request, 'league.html')