from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductModelForm

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

# def product__create__view(request, *args, **kwargs):
#     # print(request.POST)
#     # print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_form_input = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_form_input)
#                 # print("post_data ", post_data)
#     return render(request, "forms.html", {})

@staff_member_required
def product__create__view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        form = ProductModelForm()
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
        
    return render(request, "forms.html", {"form": form})

def product__list__view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)