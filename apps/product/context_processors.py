from .models import Category
from apps.vendor.models import Vendor
from apps.vendor.forms import ProductSpecForm, ProductImageForm



def menu_categories(request):
    vendor = Vendor.objects.all()
    categories = Category.objects.filter(level=0)
    """breadcrumbs_link = products.get_cat_list()
    category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
    breadcrumbs = zip(breadcrumbs_link, category_name)"""
    return {'categories':categories, 'menu_vendor_list':vendor,
            'product_spec_form':ProductSpecForm, 'product_img_form':ProductImageForm}


