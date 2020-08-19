from django.contrib import admin
from .models import Category, Product


# prepopulated_fields used to specify fields where
# the value is automatically set using the value of other fields
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # list_editable can be used for editing multiply rows at once
    # it used only after list_display attr
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
