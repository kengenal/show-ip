import csv

from django import forms
from django.utils.translation import gettext as _


class ShowIpForm(forms.Form):
    addresses = forms.CharField(widget=forms.Textarea, required=False,
                                label=_("Set website addresses, if you need more then one use ':' to separate them"))
    file = forms.FileInput()
    get_scv = forms.CheckboxInput()

    def clean(self):
        if not self.cleaned_data.get("addresses") and not self.files.get("file"):
            raise forms.ValidationError(_("Field addresses or file cannot be empty"))
        file = self.files.get("file")
        if file:
            with open(file.name) as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                data = ":".join([":".join(x) for x in reader])
                self.cleaned_data["addresses"] = data.split(":")
