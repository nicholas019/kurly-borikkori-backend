from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from products.models import Product


class ProductList(View):
    def get(self, request):
        search    = request.GET.get('search')

        products = Product.objects.filter(name__icontains = search)

        result = [
            {
                "id"   : product.id,
                "name" : product.name,
                "price": int(product.price),
                "image": product.image
            } for product in products]

        return JsonResponse({"result": result}, status = 200)



