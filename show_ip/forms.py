import csv

from django import forms
from django.utils.translation import gettext as _
from django.core.validators import URLValidator
from django.core.files.uploadedfile import SimpleUploadedFile


class ShowIpForm(forms.Form):
    addresses = forms.CharField(widget=forms.Textarea, required=False,
                                label=_("Set website addresses, if you need more then one use ':' to separate them"))
    file = forms.FileInput()
    get_scv = forms.CheckboxInput()

    def clean(self):
        if not self.cleaned_data.get("addresses") and not self.files.get("file"):
            raise forms.ValidationError(_("Field addresses or file cannot be empty"))
        file: SimpleUploadedFile = self.files.get("file")
        if file:
            validate = URLValidator()
            with open(file.name) as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                data = ":".join([":".join(x) for x in reader])
                self.cleaned_data["addresses"] = data
