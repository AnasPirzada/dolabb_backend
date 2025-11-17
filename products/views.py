"""
Product views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from products.services import ProductService, OfferService, OrderService
from products.models import Product, SavedProduct
from authentication.models import User


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    """Get products with filters"""
    filters = {
        'category': request.GET.get('category'),
        'subcategory': request.GET.get('subcategory'),
        'brand': request.GET.get('brand'),
        'minPrice': request.GET.get('minPrice'),
        'maxPrice': request.GET.get('maxPrice'),
        'size': request.GET.get('size'),
        'condition': request.GET.get('condition'),
        'search': request.GET.get('search'),
        'sortBy': request.GET.get('sortBy', 'newest')
    }
    
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))
    
    try:
        user_id = None
        if hasattr(request.user, 'id'):
            user_id = str(request.user.id)
        
        products, total = ProductService.get_products(filters, page, limit, user_id)
        
        products_list = []
        for product in products:
            is_saved = False
            if user_id:
                saved = SavedProduct.objects(user_id=user_id, product_id=product.id).first()
                is_saved = saved is not None
            
            seller = User.objects(id=product.seller_id.id).first()
            products_list.append({
                'id': str(product.id),
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'originalPrice': product.original_price,
                'images': product.images,
                'category': product.category,
                'subcategory': product.subcategory,
                'brand': product.brand,
                'size': product.size,
                'color': product.color,
                'condition': product.condition,
                'seller': {
                    'id': str(seller.id) if seller else '',
                    'username': seller.username if seller else '',
                    'profileImage': seller.profile_image if seller else ''
                },
                'isSaved': is_saved,
                'createdAt': product.created_at.isoformat()
            })
        
        return Response({
            'products': products_list,
            'pagination': {
                'currentPage': page,
                'totalPages': (total + limit - 1) // limit,
                'totalItems': total,
                'itemsPerPage': limit
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request, product_id):
    """Get product details"""
    try:
        user_id = None
        if hasattr(request.user, 'id'):
            user_id = str(request.user.id)
        
        product, is_saved, is_liked = ProductService.get_product_by_id(product_id, user_id)
        
        # Get seller - handle ReferenceField properly
        seller = None
        if product.seller_id:
            try:
                # Try to get seller_id as ObjectId
                from bson import ObjectId
                seller_obj_id = None
                
                # If seller_id is a ReferenceField that's been dereferenced
                if hasattr(product.seller_id, 'id'):
                    seller_obj_id = product.seller_id.id
                # If seller_id is already an ObjectId
                elif isinstance(product.seller_id, ObjectId):
                    seller_obj_id = product.seller_id
                # If seller_id is a string
                elif isinstance(product.seller_id, str):
                    seller_obj_id = ObjectId(product.seller_id)
                else:
                    seller_obj_id = product.seller_id
                
                if seller_obj_id:
                    seller = User.objects(id=seller_obj_id).first()
            except Exception as e:
                # If anything fails, seller will remain None
                seller = None
        
        return Response({
            'id': str(product.id),
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'originalPrice': product.original_price,
            'images': product.images,
            'category': product.category,
            'subcategory': product.subcategory,
            'brand': product.brand,
            'size': product.size,
            'color': product.color,
            'condition': product.condition,
            'tags': product.tags,
            'seller': {
                'id': str(seller.id) if seller else '',
                'username': seller.username if seller else '',
                'profileImage': seller.profile_image if seller else '',
                'rating': 0,  # TODO: Add rating system
                'totalSales': 0  # TODO: Calculate total sales
            },
            'likes': product.likes_count,
            'isLiked': is_liked,
            'isSaved': is_saved,
            'shippingInfo': {
                'cost': product.shipping_cost,
                'estimatedDays': product.processing_time_days,
                'locations': product.shipping_info.locations if product.shipping_info else []
            },
            'createdAt': product.created_at.isoformat(),
            'affiliateCode': product.affiliate_code or ''
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_product(request):
    """Create product"""
    try:
        seller_id = str(request.user.id)
        
        # Handle both single product and array of products
        data = request.data
        is_array = isinstance(data, list)
        
        if not is_array:
            data = [data]
        
        products = []
        for product_data in data:
            product = ProductService.create_product(seller_id, product_data)
            
            # Get shipping info
            shipping_info = None
            if product.shipping_info:
                shipping_info = {
                    'cost': product.shipping_info.cost,
                    'estimated_days': product.shipping_info.estimated_days,
                    'locations': product.shipping_info.locations
                }
            
            product_dict = {
                'id': str(product.id),
                'itemtitle': product.title,
                'description': product.description or '',
                'price': product.price,
                'originalPrice': product.original_price or product.price,
                'category': product.category,
                'subcategory': product.subcategory or '',
                'brand': product.brand or '',
                'currency': product.currency,
                'Quantity': product.quantity,
                'Gender': product.gender or '',
                'Size': product.size or '',
                'Condition': product.condition,
                'SKU/ID (Optional)': product.sku or '',
                'Tags/Keywords': product.tags or [],
                'Images': product.images or [],
                'Shipping Cost': product.shipping_cost,
                'Processing Time (days)': product.processing_time_days,
                'Shipping Locations': shipping_info['locations'] if shipping_info else [],
                'status': product.status,
                'seller_id': str(product.seller_id.id),
                'seller_name': product.seller_name,
                'created_at': product.created_at.isoformat() if product.created_at else None,
                'updated_at': product.updated_at.isoformat() if product.updated_at else None
            }
            
            # Add affiliate code only if it exists
            if product.affiliate_code:
                product_dict['Affiliate Code (Optional)'] = product.affiliate_code
            
            products.append(product_dict)
        
        # Return array if multiple products, single object if one product
        if len(products) == 1 and not isinstance(request.data, list):
            return Response({
                'success': True,
                'product': products[0]
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': True,
                'products': products,
                'count': len(products)
            }, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_product(request, product_id):
    """Update product"""
    try:
        seller_id = str(request.user.id)
        product = ProductService.update_product(product_id, seller_id, request.data)
        
        # Get shipping info
        shipping_info = None
        if product.shipping_info:
            shipping_info = {
                'cost': product.shipping_info.cost,
                'estimated_days': product.shipping_info.estimated_days,
                'locations': product.shipping_info.locations
            }
        
        # Build product data
        product_data = {
            'id': str(product.id),
            'itemtitle': product.title,
            'description': product.description or '',
            'price': product.price,
            'originalPrice': product.original_price or product.price,
            'category': product.category,
            'subcategory': product.subcategory or '',
            'brand': product.brand or '',
            'currency': product.currency,
            'Quantity': product.quantity,
            'Gender': product.gender or '',
            'Size': product.size or '',
            'Color': product.color or '',
            'Condition': product.condition,
            'SKU/ID (Optional)': product.sku or '',
            'Tags/Keywords': product.tags or [],
            'Images': product.images or [],
            'Shipping Cost': product.shipping_cost,
            'Processing Time (days)': product.processing_time_days,
            'Shipping Locations': shipping_info['locations'] if shipping_info else [],
            'status': product.status,
            'seller_id': str(product.seller_id.id) if hasattr(product.seller_id, 'id') else str(product.seller_id),
            'seller_name': product.seller_name,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'updated_at': product.updated_at.isoformat() if product.updated_at else None
        }
        
        # Add affiliate code only if it exists
        if product.affiliate_code:
            product_data['Affiliate Code (Optional)'] = product.affiliate_code
        
        return Response({
            'success': True,
            'product': product_data
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_product(request, product_id):
    """Delete product"""
    try:
        seller_id = str(request.user.id)
        product = ProductService.delete_product(product_id, seller_id)
        
        return Response({
            'success': True,
            'message': 'Product deleted successfully'
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_seller_products(request, seller_id):
    """Get products by seller"""
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        
        products, total = ProductService.get_seller_products(seller_id, None, page, limit)
        
        products_list = []
        for product in products:
            products_list.append({
                'id': str(product.id),
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'images': product.images,
                'status': product.status,
                'createdAt': product.created_at.isoformat()
            })
        
        return Response({
            'products': products_list,
            'pagination': {
                'currentPage': page,
                'totalPages': (total + limit - 1) // limit,
                'totalItems': total
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_product(request, product_id):
    """Save product to wishlist"""
    try:
        user_id = str(request.user.id)
        is_saved, saved = ProductService.save_product(user_id, product_id)
        
        return Response({
            'success': True,
            'isSaved': is_saved
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def unsave_product(request, product_id):
    """Remove product from wishlist"""
    try:
        user_id = str(request.user.id)
        ProductService.unsave_product(user_id, product_id)
        
        return Response({
            'success': True,
            'isSaved': False
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_products(request):
    """Get featured products"""
    try:
        limit = int(request.GET.get('limit', 10))
        page = int(request.GET.get('page', 1))
        
        user_id = None
        if hasattr(request.user, 'id'):
            user_id = str(request.user.id)
        
        products, total = ProductService.get_featured_products(limit, page, user_id)
        
        products_list = []
        for product in products:
            seller = User.objects(id=product.seller_id.id).first()
            products_list.append({
                'id': str(product.id),
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'images': product.images,
                'seller': {
                    'id': str(seller.id) if seller else '',
                    'username': seller.username if seller else '',
                    'profileImage': seller.profile_image if seller else ''
                }
            })
        
        return Response({
            'products': products_list,
            'pagination': {
                'currentPage': page,
                'totalPages': (total + limit - 1) // limit,
                'totalItems': total
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_trending_products(request):
    """Get trending products"""
    try:
        limit = int(request.GET.get('limit', 10))
        page = int(request.GET.get('page', 1))
        
        user_id = None
        if hasattr(request.user, 'id'):
            user_id = str(request.user.id)
        
        products, total = ProductService.get_trending_products(limit, page, user_id)
        
        products_list = []
        for product in products:
            seller = User.objects(id=product.seller_id.id).first()
            products_list.append({
                'id': str(product.id),
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'images': product.images,
                'seller': {
                    'id': str(seller.id) if seller else '',
                    'username': seller.username if seller else '',
                    'profileImage': seller.profile_image if seller else ''
                }
            })
        
        return Response({
            'products': products_list,
            'pagination': {
                'currentPage': page,
                'totalPages': (total + limit - 1) // limit,
                'totalItems': total
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

