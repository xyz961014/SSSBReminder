from datetime import datetime
import pytz
import requests
from pprint import pprint
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404
from .permissions import ReadOnly
from .models import ApartmentAmount, ApartmentInfo, ApartmentStatus, PersonalFilter
from .serializers import ApartmentAmountSerializer, ApartmentInfoSerializer, ApartmentStatusSerializer
from .serializers import PersonalFilterSerializer

from pathlib import Path
app_dir = Path(__file__).parent.parent.parent

class ApartmentAmountViewSet(viewsets.ModelViewSet):
    queryset = ApartmentAmount.objects.all()
    serializer_class = ApartmentAmountSerializer
    permission_classes = [ReadOnly]

class ApartmentInfoViewSet(viewsets.ModelViewSet):
    queryset = ApartmentInfo.objects.all()
    serializer_class = ApartmentInfoSerializer
    permission_classes = [ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object_number']

class ApartmentStatusViewSet(viewsets.ModelViewSet):
    queryset = ApartmentStatus.objects.all()
    serializer_class = ApartmentStatusSerializer
    permission_classes = [ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object_number']

class PersonalFilterViewSet(viewsets.ModelViewSet):
    queryset = PersonalFilter.objects.all()
    serializer_class = PersonalFilterSerializer

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

    # pprint(floors)
    
    if not floors:
        return Response({'min': None, 'max': None})

    min_floor = min(floors)
    max_floor = max(floors)

    #min_floor = 0
    #max_floor = 30
    
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

    #pprint(filter_data)

    filter_dict = {}
    if "showExpired" in filter_data.keys():
        if not filter_data["showExpired"]:
            current_time_in_stockholm = timezone.now().astimezone(pytz.timezone("Europe/Stockholm"))
            filter_dict["application_ddl__gt"] = current_time_in_stockholm

    if "validFromBefore" in filter_data.keys() and filter_data["validFromBefore"] is not None:
        valid_from_before = datetime.strptime(filter_data["validFromBefore"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
        filter_dict["valid_from__lte"] = valid_from_before

    if "selectedRegion" in filter_data.keys() and len(filter_data["selectedRegion"]) > 0:
        filter_dict["housing_area__in"] = filter_data["selectedRegion"]

    if "selectedType" in filter_data.keys() and len(filter_data["selectedType"]) > 0:
        filter_dict["accommodation_type__in"] = filter_data["selectedType"]

    if "spaceRange" in filter_data.keys() and len(filter_data["spaceRange"]) == 2:
        filter_dict["living_space__gte"] = filter_data["spaceRange"][0]
        filter_dict["living_space__lte"] = filter_data["spaceRange"][1]

    if "rentRange" in filter_data.keys() and len(filter_data["rentRange"]) == 2:
        filter_dict["monthly_rent__gte"] = filter_data["rentRange"][0]
        filter_dict["monthly_rent__lte"] = filter_data["rentRange"][1]

    if "floorRange" in filter_data.keys() and len(filter_data["floorRange"]) == 2:
        filter_dict["floor__gte"] = filter_data["floorRange"][0]
        filter_dict["floor__lte"] = filter_data["floorRange"][1]

    if "electricityIncluded" in filter_data.keys() and filter_data["electricityIncluded"] != "":
        filter_dict["electricity_include__in"] = [filter_data["electricityIncluded"] == "true"]

    if "summerFree" in filter_data.keys() and filter_data["summerFree"] != "":
        filter_dict["rent_free_june_and_july__in"] = [filter_data["summerFree"] == "true"]

    if "max4Years" in filter_data.keys() and filter_data["max4Years"] != "":
        filter_dict["max_4_years__in"] = [filter_data["max4Years"] == "true"]

    if "shortRent" in filter_data.keys() and filter_data["shortRent"] != "":
        filter_dict["end_date__isnull"] = filter_data["shortRent"] == "false"

    filtered_apartments = ApartmentInfo.objects.filter(**filter_dict)

    if "creditRange" in filter_data.keys() and len(filter_data["creditRange"]) == 2:
        credit_min = filter_data["creditRange"][0]
        credit_max = filter_data["creditRange"][1]
        filtered_apartments = [a for a in filtered_apartments 
                               if a.bid is None or credit_min < a.bid['most_credit'] < credit_max]

    #credits = [a.bid for a in filtered_apartments]
    #pprint(filtered_apartments[0].application_ddl)

    serializer = ApartmentInfoSerializer(filtered_apartments, many=True)
    return Response(serializer.data)

#@api_view(['GET'])
#def get_bid_history(request):
#    object_number = None
#    if "object_number" in request.data.keys():
#        object_number = request.data["object_number"]
#    
#    credits = [apartment.bid["most_credit"] for apartment in apartments if apartment.bid is not None]
#    
#    if not credits:
#        return Response({'min': None, 'max': None})
#
#    min_credit = min(credits)
#    max_credit = max(credits)
#    
#    return Response({'min': min_credit, 'max': max_credit})

@api_view(['GET'])
def get_drawing(request):
    object_number = None
    drawing_type = "APARTMENT"
    if "object_number" in request.GET:
        object_number = request.GET["object_number"]
    if "drawing_type" in request.GET:
        drawing_type = request.GET["drawing_type"]

    file_path = app_dir / "resources" / f"{object_number}_{drawing_type} DRAWING.pdf"

    print(file_path, file_path.exists())

    if not file_path.exists():
        raise Http404("File not found")

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


@api_view(['GET'])
def get_geocode(request):
    address = request.GET.get('address')
    
    if not address:
        return Response({'error': 'Address parameter is required'}, status=400)
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return Response(data)
    
    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)
