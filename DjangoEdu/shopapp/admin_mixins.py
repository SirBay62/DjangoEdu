import csv
from dataclasses import field

from django.db.models.options import Options
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse


class ExportAsMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [fieid.name for fieid in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name}".csv'

        csv_writer = csv.writer(response)

        csv_writer.writerow(field_names)
        for obj in queryset:
            csv_writer.writerow([getattr(obj,fieid) for fieid in field_names])
        return response
    export_csv.short_description = "Export as CSV"