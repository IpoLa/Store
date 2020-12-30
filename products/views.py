from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Product, ProductLike
from .forms import ProductModelForm
from emails.forms import InventoryWaitlistForm

from .serializer import (
    ProductSerializer, 
    ProductActionSerializer, 
    ProductCreateSerializer
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


# Create your views here.

def featured_product_view(request, *args, **kwargs):
    qs = Product.objects.filter(featured=True)
    product = None
    form = None
    can_order = False
    if qs.exists():
        product = qs.first()
    if product != None:
        can_order = product.can_order
        if can_order:
            product_id = product.id
            request.session['product_id'] = product_id
        form = InventoryWaitlistForm(request.POST or None, product=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return redirect("/waitlist-success")
    context = {
        "object": product,
        "form": form,
        "can_order": can_order,
        # "has_inventory": product.has_inventory()
    }
    return render(request, "products/detail.html", context)

def home__view(request, *args, **kwargs):
    context = {"name": "Akram"}
    return render(request, "home.html", context)
 
def product__detail__view_pure_django(request, pk):
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




#  TRY REST FRAMEROWK
@api_view(['POST'])  # http method the client == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def product__create__view(request, *args, **kwargs):
    serializer = ProductCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=False):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def product__list__view(request, *args, **kwargs):
    qs = Product.objects.all()
    serializer = ProductSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product__detail__view(request, id, *args, **kwargs):
    qs = Product.objects.filter(id=id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = ProductSerializer(obj)
    return Response(serializer.data)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def product__delete__view(request, id, *args, **kwargs):
    qs = Product.objects.filter(id=id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this product."}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Product removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product__action__view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike
    '''
    serializer = ProductActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        product_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Product.objects.filter(id=product_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = ProductSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = ProductSerializer(obj)
            return Response(serializer.data, status=200)

    return Response({"message": "Product liked"}, status=200)


@staff_member_required   # Can use this @staff_member_required to select permissions
def product__create__view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View
    '''
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # Product image/video
        image = request.FILES.get('image')
        media = request.FILES.get('media')
        # Do some stuff
        if image:
            obj.image = image
        if media:
            obj.media = media

        obj.user = request.user
        obj.save()
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        form = ProductModelForm()
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
        
    return render(request, "forms.html", {"form": form})

def product__list__view_pure_django(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)