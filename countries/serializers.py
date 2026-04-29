from rest_framework import serializers
from .models import Country, CountryEntry, TravelItem, Region


class CountrySerializer(serializers.ModelSerializer):
    continent_display = serializers.CharField(source='get_continent_display', read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_code', 'continent', 'continent_display',
                  'flag_emoji', 'capital', 'region', 'numeric_code']


class TravelItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    region_name = serializers.SerializerMethodField()
    country_name = serializers.CharField(source='country_entry.country.name', read_only=True)
    country_iso = serializers.CharField(source='country_entry.country.iso_code', read_only=True)
    country_entry_id = serializers.IntegerField(source='country_entry.id', read_only=True)

    class Meta:
        model = TravelItem
        fields = ['id', 'category', 'category_display', 'name', 'is_done',
                  'region', 'region_name', 'country_name', 'country_iso','country_entry_id','created_at']
        read_only_fields = ['id', 'created_at']

    def get_region_name(self, obj):
        return obj.region.name if obj.region else None

    def get_region_name(self, obj):
        if obj.region:
            return obj.region.name
        return None


class RegionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'name', 'type', 'type_display', 'notes', 'item_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_item_count(self, obj):
        return obj.items.count()


class RegionDetailSerializer(RegionSerializer):
    items = TravelItemSerializer(many=True, read_only=True)

    class Meta(RegionSerializer.Meta):
        fields = RegionSerializer.Meta.fields + ['items']


class CountryEntrySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = CountryEntry
        fields = [
            'id', 'country', 'country_id', 'status', 'status_display',
            'visited_at', 'notes', 'item_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_item_count(self, obj):
        return obj.items.count()

    def validate(self, data):
        user = self.context['request'].user
        country = data.get('country')
        if self.instance is None:
            if CountryEntry.objects.filter(user=user, country=country).exists():
                raise serializers.ValidationError(
                    f"You already have an entry for {country.name}."
                )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CountryEntryDetailSerializer(CountryEntrySerializer):
    items = TravelItemSerializer(many=True, read_only=True)
    regions = RegionSerializer(many=True, read_only=True)

    class Meta(CountryEntrySerializer.Meta):
        fields = CountryEntrySerializer.Meta.fields + ['items', 'regions']