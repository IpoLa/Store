from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import Product
# Create your views here.

def home__view(request, *args, **kwargs):
    context = {"name": "Akram"}
    return render(request, "home.html", context)
 
def product__detail__view(request, pk):
    try: 
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404               # Can render HTML Page, with HTTP code of 404

        #  The user don't need to know the problem here
    # try:
    #     obj = Product.objects.get(id=id)
    # except:
    #     raise Http404

    # return HttpResponse(f"Product id {obj.id}")
    # return render(request, "products/product_detail.html", {"object": obj})
    return render(request, "products/detail.html", {"object": obj})

def product__api__detail__view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=404) 
    return JsonResponse({"id ": obj.id})

def search__view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"home": "abc", "query": query}
    return render(request, "home.html", context)

def product__create__view(request, *args, **kwargs):
    # print(request.POST)
    # print(request.GET)
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            print("post_data ", post_data)
    return render(request, "forms.html", {})

def product__list__view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)