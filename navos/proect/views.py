from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import permissions
from .permissions import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =[permissions.IsAdminUser]

class ProductViewSet(viewsets.ViewSet):
    # permission_classes = [ProductPermission]
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,methods=['get'])
    def products_search(self,request):
        query = request.query_params.get('q')
        if query is None:
            return Response({'message':'Ничего не найдено'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(name__icontains =query)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    @action(detail=False,methods=['get'])
    def search_by_category(self,request):
        query = request.query_params.get('category')
        if query is None:
            return Response({'message':'Ничего не найдено'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(category=query)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=['get'])
    def get_all_reviews(self,request):
        try:
            query = request.query_params.get('id')
            reviews = Review.objects.filter(product=query)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'message': 'Ошибка'}, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.ViewSet):
    # permission_classes = [UserPermission]
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def del_product(self, request):
        try:
            query = request.query_params.get('id')
            product_query = request.GET.get('name')
            user = User.objects.get(pk=query)
            user_cart_list = User.objects.get(pk=query).cart.all()
            user_list = list(user_cart_list)
            if len(user_list)!=0:
                position = 0
                for i in user_list:
                    if product_query== i.name:
                        position =user_list.index(i)
                        break
                user_list.pop(position)
                user.cart.set(user_list)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                user.cart.set(user_list)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            
        except User.DoesNotExist:
            return Response({'message':'shit'},status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'])
    def add_to_cart(self, request):
        try:
            query = request.query_params.get('id')
            prod_query = request.GET.get('q')
            user_query = User.objects.get(pk=query)
            user_cart = User.objects.get(pk=query).cart.all()
            product = Product.objects.get(pk=prod_query)
            user_cart_list = list(user_cart)
            user_cart_list.append(product)
            user_query.cart.set(user_cart_list)
            serializer = UserSerializer(user_query)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'])
    def get_orders(self, request):
        try:
            query = request.query_params.get('id')
            order = Order.objects.filter(owner=query)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "закази нет"}, status=status.HTTP_404_NOT_FOUND)
        
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ViewSet):
    # permission_classes = [ReviewPermission]
    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = UserSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def add_rating(self,request):
        try:
            query = request.query_params.get('q')
            product = Product.objects.get(pk=query)
            review_filter = Review.objects.filter(product=query)
            review_list = list(review_filter)
            arithmetic_mean = 0
            print(review_list)
            for i in review_list:
                arithmetic_mean += i.rating
            review_mean = round(arithmetic_mean/int(len(review_list)))
            product.rating = review_mean
            product.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data)
            # return Response({'message':'Рейтинг установлен'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



# Create your views here.
