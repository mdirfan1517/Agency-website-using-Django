from django.contrib import admin
from app.models import (
    GeneralInfo,
    Service,
    Testimonial,
    ContactFormLog,
    Author,
    Blog
)
from django.utils.html import format_html

@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    

    list_display=[
        'company_name',
        'location',
        'email',
        'phone',
        'open_hours',
    ]

    # readonly_fields=[
    #     'email'

    # ]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display=[
        "title",
        "description"
    ]

    search_fields=[
        "title",
        "description"
    ]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'company_name',
        'user_job_title',
        'location',
        'display_rating_count',
        'created_at'
    ]
    
    list_filter = ['rating_count', 'location', 'created_at']
    search_fields = ['username', 'company_name', 'user_job_title', 'review']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'user_job_title', 'user_image')
        }),
        ('Company Information', {
            'fields': ('company_name', 'location')
        }),
        ('Review Details', {
            'fields': ('rating_count', 'review', 'created_at')
        }),
    )

    def display_rating_count(self, obj):
        return '★' * obj.rating_count
    
    display_rating_count.short_description = "Rating"

@admin.register(ContactFormLog)
class ContactFormLogAdmin(admin.ModelAdmin):
    

    list_display=[
        'email',
        'is_success',
        'is_error',
        'action_time',
        
    ]

    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    

    list_display=[
        
        'first_name',
        'last_name',
        
    ]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'author',
        'is_featured',
        'views_count',
        'created_at'
    ]
    
    list_filter = ['category', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'summary', 'tags']
    readonly_fields = ['views_count', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'blog_image', 'author')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'tags')
        }),
        ('Settings', {
            'fields': ('is_featured', 'views_count', 'created_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new blog post
            obj.author = request.user.author if hasattr(request.user, 'author') else None
        super().save_model(request, obj, form, change)

