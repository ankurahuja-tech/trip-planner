from rest_framework_gis import serializers as gis_serializers

from .models import Marker


class MarkerSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Marker GeoJSON serializer."""

    class Meta:

        fields = (
            "id",
            "user",
            "trip",
            "name",
        )
        geo_field = "geom"
        model = Marker
