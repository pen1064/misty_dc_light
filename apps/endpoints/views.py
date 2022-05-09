from django.shortcuts import render
from rest_framework import views, mixins, viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from apps.endpoints.models import Endpoints, MLAlgorithm, MLRequest
from apps.endpoints.serializers import EndpointsSerializer, MLAlgorithmSerializer, MLRequestSerializer
from apps.ml.registry import MLRegistry
from misty_dc.wsgi import registry
from django.db import transaction
from apps.ml.classifier.xgb_model import XGBClassifier
import json
class EndpointsViewSet( mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointsSerializer
    queryset = Endpoints.objects.all()


class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()

class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

class PredictView(views.APIView):

    def post(self, request, endpoint_name='classifier', format=None):
        print(self.request.query_params.get('endpoint'))
        print(self.request.data)
        alg_status = self.request.query_params.get('status', 'production')
        alg_version = self.request.query_params.get('version')
        print(alg_version)
        #alg = MLAlgorithm.objects.filter(parent_endpoint__name = endpoint_name)
        alg = MLAlgorithm.objects.filter(parent_endpoint__name = endpoint_name)
        print(alg)
        # update version
        if alg_version is not None:
            alg = alg.filter(version=alg_version)

        if len(alg) == 0:
            return Response({'status':'error', 'message': 'no ml available'}, status=status.HTTP_400_BAD_REQUEST)
        print(alg)
        print(registry.endpoints)

        alg_index = 0
        #alg_obj = XGBClassifier()
        alg_obj = registry.endpoints
        prediction = alg_obj.predict(self.request.data)
        label = prediction['label'] if 'label' in prediction else 'error_gg'
        mlrequest = MLRequest(input_data=json.dumps(request.data), full_response=prediction, 
        response=label,parent_mlalgorithm=alg[alg_index])

        mlrequest.save()
        prediction['request_id'] = mlrequest.id

        return Response(prediction)