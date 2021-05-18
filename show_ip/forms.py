import csv
import itertools
import io
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class ShowIpForm(forms.Form):
    addresses = forms.CharField(
        label=None,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control",
                                     "placeholder": _("Url address, you can take many urls using ':' as separator"),
                                     'rows': 1, 'cols': 15})
    )
    file = forms.FileField(
        label=_("Load from csv file"),
        widget=forms.ClearableFileInput(attrs={"multiple": False, "class": "form-control"}),
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=["csv"], message=_("Not supported file"))]
    )
    get_scv = forms.BooleanField(
        label=_("Download csv file"), required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def clean(self):
        if self.cleaned_data.get("addresses"):
            self.cleaned_data["addresses"] = self.cleaned_data["addresses"].split(",")
        if file := self.cleaned_data.get("file"):
            with io.TextIOWrapper(file.file) as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                data = list(itertools.chain(*reader))
                clear = [x.strip() for x in data if x]
                self.cleaned_data["addresses"] = clear
        if not self.cleaned_data.get("addresses") and not self.files.get("file"):
            raise forms.ValidationError(_("Field addresses or file cannot be empty"))
