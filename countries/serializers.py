from rest_framework import serializers
from .models import Country, CountryEntry, TravelItem


class CountrySerializer(serializers.ModelSerializer):
    continent_display = serializers.CharField(source='get_continent_display', read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_code', 'continent', 'continent_display',
                  'flag_emoji', 'capital', 'region']


class TravelItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TravelItem
        fields = ['id', 'category', 'category_display', 'name', 'notes', 'is_done', 'created_at']
        read_only_fields = ['id', 'created_at']


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

    class Meta(CountryEntrySerializer.Meta):
        fields = CountryEntrySerializer.Meta.fields + ['items']