import json
from json import JSONDecodeError

from show_ip.forms import ShowIpForm
from show_ip.views import BestShowView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ShowIpAPIView(BestShowView):
    form_class = ShowIpForm

    def post(self, request):
        try:
            status = 200
            data = json.loads(request.body) if request.is_ajax else {}
            context = self.form_validate(post_data=data, post_files=request.FILES)
            if isinstance(context, HttpResponse):
                return context
            form = context.pop("form")
            if form.errors:
                context["errors"] = form.errors
                status = 400
            return JsonResponse(context, status=status)
        except (TypeError, JSONDecodeError):
            return JsonResponse({"TypeError": "Type not supported"}, status=400)
