from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .permissions import ReadOnly
from .models import ApartmentAmount
from .serializers import ApartmentAmountSerializer

class ApartmentAmountViewSet(viewsets.ModelViewSet):
    queryset = ApartmentAmount.objects.all()
    serializer_class = ApartmentAmountSerializer
    permission_classes = [ReadOnly]

@api_view(['GET'])
def get_status(request):
    try:
        status = ApartmentAmount.objects.latest('_id')
    except ApartmentAmount.DoesNotExist:
        return Response({'error': 'No status available'}, status=404)
    
    serializer = ApartmentAmountSerializer(status)
    return Response(serializer.data)


class IndexView(TemplateView):
    template_name = 'index.html'
