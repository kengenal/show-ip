import csv
import itertools

from django import forms
from django.utils.translation import gettext_lazy as _


class ShowIpForm(forms.Form):
    addresses = forms.CharField(
        label=None, required=False,
        widget=forms.Textarea(attrs={"class": "form-control",
                                     "placeholder": _("Url address, you can take many urls using ':' as separator"),
                                     'rows': 1, 'cols': 15})
    )
    file = forms.FileField(label=_("Load from csv file"),
                           widget=forms.ClearableFileInput(attrs={"multiple": False, "class": "form-control"}),
                           required=False)
    get_scv = forms.BooleanField(
        label=_("Download csv file"), required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    def clean(self):
        if self.cleaned_data.get("addresses"):
            self.cleaned_data["addresses"] = self.cleaned_data["addresses"].split(",")
        if file := self.files.get("file"):
            with open(file.name) as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                data = list(itertools.chain(*reader))
                self.cleaned_data["addresses"] = data

        if not self.cleaned_data.get("addresses") and not self.files.get("file"):
            raise forms.ValidationError(_("Field addresses or file cannot be empty"))
