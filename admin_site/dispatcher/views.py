from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.template.response import TemplateResponse
from django.db.models import Count
from dispatcher.models import Request, House
from dispatcher.forms import StatusChangeForm, RequestFilterForm
from dispatcher.services import notify_resident


class RequestListView(ListView):
    model = Request
    template_name = "dispatcher/request_list.html"
    context_object_name = "requests"
    paginate_by = 20

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["dispatcher/_request_table.html"]
        return [self.template_name]

    def get_queryset(self):
        qs = Request.objects.select_related("house")

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        house = self.request.GET.get("house")
        if house:
            qs = qs.filter(house_id=house)

        req_type = self.request.GET.get("type")
        if req_type:
            qs = qs.filter(type=req_type)

        search = self.request.GET.get("search", "").strip()
        if search:
            try:
                qs = qs.filter(number=int(search))
            except (ValueError, TypeError):
                qs = qs.none()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["filter_form"] = RequestFilterForm(self.request.GET)
        ctx["search"] = self.request.GET.get("search", "")

        status_counts = dict(
            Request.objects.values_list("status").annotate(cnt=Count("pk"))
        )
        ctx["status_counts"] = {
            s: status_counts.get(s, 0) for s, _ in Request.STATUS_CHOICES
        }
        ctx["status_counts"]["all"] = Request.objects.count()
        ctx["status_choices"] = Request.STATUS_CHOICES
        return ctx


class RequestDetailView(DetailView):
    model = Request
    template_name = "dispatcher/request_detail.html"
    context_object_name = "request"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = StatusChangeForm(instance=self.object)
        return ctx

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data(object=self.object)
        return TemplateResponse(request, self.template_name, ctx)

    def post(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        old_status = req.status
        form = StatusChangeForm(request.POST, instance=req)

        if form.is_valid():
            updated = form.save()
            if updated.status != old_status:
                notify_resident(updated)
            ctx = self.get_context_data(object=updated)
            return TemplateResponse(request, self.template_name, ctx)

        ctx = self.get_context_data(object=req)
        ctx["form"] = form
        return TemplateResponse(request, self.template_name, ctx)


class DigestView(TemplateView):
    template_name = "dispatcher/digest.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = Request.objects.all()
        ctx["total"] = today.count()
        ctx["by_category"] = dict(
            today.values_list("type").annotate(cnt=Count("pk"))
        )
        ctx["by_sentiment"] = dict(
            today.values_list("sentiment").annotate(cnt=Count("pk"))
        )
        ctx["by_status"] = dict(
            today.values_list("status").annotate(cnt=Count("pk"))
        )
        ctx["top_houses"] = (
            today.values("house__name")
            .annotate(cnt=Count("pk"))
            .order_by("-cnt")[:5]
        )
        ctx["status_choices"] = Request.STATUS_CHOICES
        return ctx


class HousesView(TemplateView):
    template_name = "dispatcher/houses.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["houses"] = House.objects.annotate(req_count=Count("requests"))
        return ctx


class SettingsView(TemplateView):
    template_name = "dispatcher/settings.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["settings_mock"] = {
            "director_tg_id": "100500",
            "daily_report_time": "18:00",
            "alert_threshold": "3",
            "llm_model": "gpt-4o-mini",
        }
        return ctx
