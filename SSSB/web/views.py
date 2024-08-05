from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .permissions import ReadOnly
from .models import ApartmentAmount, ApartmentInfo
from .serializers import ApartmentAmountSerializer, ApartmentInfoSerializer

class ApartmentAmountViewSet(viewsets.ModelViewSet):
    queryset = ApartmentAmount.objects.all()
    serializer_class = ApartmentAmountSerializer
    permission_classes = [ReadOnly]

class ApartmentInfoViewSet(viewsets.ModelViewSet):
    queryset = ApartmentInfo.objects.all()
    serializer_class = ApartmentInfoSerializer
    permission_classes = [ReadOnly]

class IndexView(TemplateView):
    template_name = 'index.html'

@api_view(['GET'])
def get_status(request):
    try:
        status = ApartmentAmount.objects.latest('_id')
    except ApartmentAmount.DoesNotExist:
        return Response({'error': 'No status available'}, status=404)
    
    serializer = ApartmentAmountSerializer(status)
    return Response(serializer.data)

@api_view(['GET'])
def get_regions(request):
    regions = ApartmentInfo.objects.values_list('housing_area', flat=True).distinct()
    return Response(regions)

@api_view(['GET'])
def get_types(request):
    types = ApartmentInfo.objects.values_list('accommodation_type', flat=True).distinct()
    return Response(types)

@api_view(['GET'])
def get_space_range(request):
    apartments = ApartmentInfo.objects.all()
    
    living_spaces = [apartment.living_space for apartment in apartments if apartment.living_space is not None]
    
    if not living_spaces:
        return Response({'min': None, 'max': None})

    min_living_space = min(living_spaces)
    max_living_space = max(living_spaces)
    
    return Response({'min': min_living_space, 'max': max_living_space})

@api_view(['GET'])
def get_rent_range(request):
    apartments = ApartmentInfo.objects.all()
    
    rents = [apartment.monthly_rent for apartment in apartments if apartment.monthly_rent is not None]
    
    if not rents:
        return Response({'min': None, 'max': None})

    min_rent = min(rents)
    max_rent = max(rents)
    
    return Response({'min': min_rent, 'max': max_rent})

@api_view(['GET'])
def get_floor_range(request):
    apartments = ApartmentInfo.objects.all()
    
    floors = [apartment.floor for apartment in apartments if apartment.floor is not None]
    
    if not floors:
        return Response({'min': None, 'max': None})

    min_floor = min(floors)
    max_floor = max(floors)
    
    return Response({'min': min_floor, 'max': max_floor})



@api_view(['GET'])
def get_credit_range(request):
    apartments = ApartmentInfo.objects.all()
    
    credits = [apartment.bid["most_credit"] for apartment in apartments if apartment.bid is not None]
    
    if not credits:
        return Response({'min': None, 'max': None})

    min_credit = min(credits)
    max_credit = max(credits)
    
    return Response({'min': min_credit, 'max': max_credit})

@api_view(['POST'])
def get_filtered_apartments(request):
    filter_data = request.data

    filter_dict = {}
    if "spaceRange" in filter_data.keys() and len(filter_data["spaceRange"]) == 2:
        filter_dict["living_space__gte"] = filter_data["spaceRange"][0]
        filter_dict["living_space__lte"] = filter_data["spaceRange"][1]

    filtered_apartments = ApartmentInfo.objects.filter(**filter_dict)

    serializer = ApartmentInfoSerializer(filtered_apartments, many=True)
    return Response(serializer.data)
