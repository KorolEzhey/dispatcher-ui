from django import forms
from dispatcher.models import Request


class StatusChangeForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["status", "comment_to_resident", "internal_comment"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "comment_to_resident": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Будет отправлено жителю"}
            ),
            "internal_comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Внутренний, жителю не виден"}
            ),
        }
        labels = {
            "status": "Статус",
            "comment_to_resident": "Комментарий жителю",
            "internal_comment": "Внутренний комментарий",
        }


class RequestFilterForm(forms.Form):
    house = forms.IntegerField(required=False, widget=forms.Select(attrs={"class": "form-select"}))
    type = forms.CharField(required=False, widget=forms.Select(attrs={"class": "form-select"}))

    def __init__(self, *args, **kwargs):
        from dispatcher.models import House

        super().__init__(*args, **kwargs)
        self.fields["house"].widget.choices = [("", "Все дома")] + list(
            House.objects.values_list("pk", "name")
        )
        self.fields["type"].widget.choices = [("", "Все типы")] + list(Request.TYPE_CHOICES)
