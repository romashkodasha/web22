from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Max, Min
from dance.serializers import ClassSerializer
from dance.serializers import StudentsSerializer
from dance.serializers import PurchaseSerializer
from dance.models import Class
from dance.models import Students
from dance.models import Purchase


class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать группы
    """
    serializer_class = ClassSerializer  # Сериализатор для модели
    filter_backends = [filters.SearchFilter]
    search_fields = ['trainer']
    def get_queryset(self):
        queryset = Class.objects.all()
        min_price = self.request.query_params.get('minPrice')
        max_price = self.request.query_params.get('maxPrice')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset
    # Class.objects.aggregate(Max('price'))
    # @action(detail=False)
    # def min_price(self,request):
    #     res=Class.objects.aggregate(Min('price'))
    #     serializer = self.get_serializer(res)
    #     return Response(serializer.data)

@api_view(['GET'])
def priceRange(request):
    return Response(Class.objects.aggregate(price_min=Min('price'), price_max=Max('price')))

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
