from django.shortcuts import render
from .models import Journal, Category
from django.db.models import Q

def FilterView(request):
    qs = Journal.objects.all()
    categories = Category.objects.all()
    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('id_exact')
    title_or_author_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    notReviewed = request.GET.get('notReviewed')

    #The i in icontains means case insensitive
    if title_contains_query != '' and title_contains_query is not None:
        qs = qs.filter(title__icontains=title_contains_query)
    
    elif id_exact_query != '' and id_exact_query is not None:
        qs = qs.filter(id=id_exact_query)

    #If the same Journal is found in both OR statements then we only want to return one
    #of them - use .distinct()
    elif title_or_author_query != '' and title_or_author_query is not None:
        qs = qs.filter(Q(title__icontains=title_or_author_query)
                       | Q(author__name__icontains=title_or_author_query)
                       ).distinct()

    if view_count_min != '' and view_count_min is not None:
        qs = qs.filter(views__gte=view_count_min)
    
    if view_count_max != '' and view_count_max is not None:
        qs = qs.filter(views__lt=view_count_max)
    
    if date_min != '' and date_min is not None:
        qs = qs.filter(publish_date__gte=date_min)
    
    if date_max != '' and date_max is not None:
        qs = qs.filter(publish_date__lt=date_max)
    
    if category != '' and category is not None and category != 'Choose...':
        qs =qs.filter(categories__name=category)
    
    if reviewed == 'on':
        qs =qs.filter(reviewed=True)
    elif notReviewed == 'on':
        qs = qs.filter(reviewed=False)
    
    
    context = {
        'queryset':qs,
        'categories':categories
    }
    return render(request, "search.html", context)

