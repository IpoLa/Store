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

    return HttpResponse(f"Product id {obj.id}")

def product__api__detail__view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=404) 
    return JsonResponse({"id ": obj.id})