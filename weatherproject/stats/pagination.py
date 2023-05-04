import coreapi
import coreschema.schemas
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    def get_schema_fields(self, view):
        fields = super(CustomPagination, self).get_schema_fields(view)
        fields.extend(
            [
                coreapi.Field('year',  description="Year", location='query', schema=coreschema.schemas.Integer(), required=True, example=None, type=None),
                coreapi.Field('station_code', description="Station Code",  location='query',
                              required=True, example=None, type=None, schema=coreschema.schemas.String()),
            ]
        )
        return fields
