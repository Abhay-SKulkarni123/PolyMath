from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):
    """
    Allow access only to approved vendors.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'vendor' and
            hasattr(request.user, 'vendor_profile') and
            request.user.vendor_profile.is_approved
        )
    
class IsAdmin(BasePermission):
    """
       Allow access only to admin.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
        
class IsVendorOrAdmin(BasePermission):
    """
    Allow access to vendors or admins.
    """
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            request.user.role in ['vendor', 'admin']
        )
    
class IsOwnerOrAdmin(BasePermission):
    """
    Object level permission.
    Only the owner of an object or admin can modify it.
    """
    def has_object_permission(self, request, view, obj):
        if request.use.role == 'admin':
            return True
        return obj.vendor.user == request.user
    