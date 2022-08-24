from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from tips.models import Tip


# /tip/list
class TipListView(View):
    def get(self, request):
        tag    = request.GET.get('tag')
        sort   = int(request.GET.get('sort', 1))
        search = request.GET.get('search')

        if sort > 4:
            sort_set = {
                1 : "-id",
                2 : "-hit",
                3 : "-tiplike__tip_id",
            }
            tip_list = Tip.objects.all().select_related('user').order_by(sort_set[sort])
        else:
            tip_list = Tip.objects.all().select_related('user').order_by("-hit","-tiplike__tip")

        if search:
            if tag == 1:
                tip_list = tip_list.filter(title__icontains = search)
            elif tag == 2:
                tip_list = tip_list.filter(
                    Q(content__content__icontains=search)|\
                    Q(hashtag__name__icontains=search)|\
                    Q(intro__country__icontains=search)
                    )
            elif tag == 3:
                tip_list = tip_list.filter(
                    Q(title__icontains=search)|\
                    Q(content__content__icontains=search)|\
                    Q(hashtag__name__icontains=search)|\
                    Q(intro__country__icontains=search))        
            else: 
                tip_list = tip_list.filter(user__name__icontains=search)   

        result = [{
            "id"             : tip.id,
            "title"          : tip.title,
            "tip_thumbnauil" : tip.thumbnail,
            "user_id"        : tip.user.id,
            "user_thumbnauil": tip.user.thumbnail,
            "uesr_name"      : tip.user.name
        }for tip in tip_list]

        return JsonResponse({"result": result}, status = 200)


