from rest_framework import serializers
from apps.endpoints.models import Endpoints, MLAlgorithm, MLRequest

class EndpointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoints
        read_only_fields = ('id', 'name', 'owner', 'created_date')
        fields = read_only_fields

class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        read_only_fields=('id', 'name', 'code','description', 'version', 'created_date', 'parent_endpoint', 'status')
        fields = read_only_fields

    
class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ("id","input_data","response","full_response",
        "created_date", "parent_mlalgorithm")

        fields =  ("id","input_data","response","full_response",
        "created_date", "parent_mlalgorithm")