import csv
import itertools

from django import forms
from django.utils.translation import gettext as _


class ShowIpForm(forms.Form):
    addresses = forms.CharField(widget=forms.Textarea, required=False,
                                label=_("Set website addresses, if you need more then one use ':' to separate them"))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": False}), required=False)
    get_scv = forms.BooleanField(required=False)

    def clean(self):
        if self.cleaned_data.get("addresses"):
            self.cleaned_data["addresses"] = self.cleaned_data["addresses"].split(":")
        if file := self.files.get("file"):
            with open(file.name) as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                data = list(itertools.chain(*reader))
                self.cleaned_data["addresses"] = data

        if not self.cleaned_data.get("addresses") and not self.files.get("file"):
            raise forms.ValidationError(_("Field addresses or file cannot be empty"))
