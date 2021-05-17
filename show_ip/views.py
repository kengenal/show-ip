import csv

from django.shortcuts import render
from django.views import generic
from show_ip.forms import ShowIpForm
from show_ip.services import generate
from django.http import HttpResponse


def get_ips(hostnames):
    return [x for x in generate(hostnames)]


class ShowIpView(generic.View):
    form_class = ShowIpForm
    template_name = "show_ip/index.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            clean = form.cleaned_data.get("addresses", [])
            context["ips"] = get_ips(clean)
            if form.cleaned_data.get("get_scv"):
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="host.csv"'},
                )
                writer = csv.writer(response)
                writer.writerow(["host", "port", "ssl", "errors"])
                for x in context["ips"]:
                    writer.writerow([x.get("host"), x.get("port"), x.get("ssl"), x.get("errors")])
                return response
        context["form"] = form
        return render(request, self.template_name, context)
