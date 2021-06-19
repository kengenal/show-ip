import csv
from abc import ABC

from django.shortcuts import render
from django.views import generic
from show_ip.forms import ShowIpForm
from show_ip.services import generate
from django.http import HttpResponse


def get_ips(hostnames):
    return [x for x in generate(hostnames)]


class BestShowView(ABC, generic.View):
    form_class = ShowIpForm

    def form_validate(self, post_data, post_files):
        form = self.form_class(data=post_data, files=post_files)
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
                writer.writerow(["host", "ip", "port", "ssl", "errors"])
                for x in context["ips"]:
                    writer.writerow([x.get("host"), x.get("ip"), x.get("port"), x.get("ssl", "OK"),
                                     x.get("errors", "-")])
                return response
        context["form"] = form
        return context


class ShowIpView(BestShowView):
    form_class = ShowIpForm
    template_name = "show_ip/index.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        context = self.form_validate(post_data=request.POST, post_files=request.FILES)
        if isinstance(context, HttpResponse):
            return context
        return render(request, self.template_name, context)
