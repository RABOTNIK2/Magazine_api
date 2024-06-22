from rest_framework import permissions
class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            return True
        elif view.action in ['update', 'destroy', 'del_product', 'add_product']:
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'update', 'destroy', 'del_product', 'add_product']:
            return obj == request.user or request.user.is_staff
        else:
            return False

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'products_search', 'search_by_category']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', 'products_search', 'search_by_category']:
            return obj == request.user or request.user.is_staff
        elif view.action in ['create', 'update', 'destroy']:
            return obj == request.user.is_staff
        else:
            return False

class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy', 'add_rating']:
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['create', 'update', 'destroy', 'add_rating']:
            return obj == request.user or request.user.is_staff
        else:
            return False