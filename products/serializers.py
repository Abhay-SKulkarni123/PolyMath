from rest_framework import serializers
from .models import KnowledgeField, Product

class KnowledgeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeField
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color']

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.store_name', read_only=True)
    knowledge_fields = KnowledgeFieldSerializer(many=True, read_only=True)
    knowledge_field_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=KnowledgeField.objects.all(), source='knowledge_fields')
    is_digital = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id',
            'vendor_name',
            'knowledge_fields',
            'knowledge_field_ids',
            'name',
            'description',
            'price',
            'stock',
            'type',
            'file',
            'is_digital',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'vendor_name', 'created_at', 'is_digital']

    def validate(self, attrs):
        product_type = attrs.get('type', 'physical')
        file = attrs.get('file')
        if product_type == 'digital' and not file:
            raise serializers.ValidationError(
                {'file' : 'Digital Products must include a file upload.'}
            )
        return attrs