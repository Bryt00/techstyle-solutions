from django.contrib import admin
from django.utils.html import format_html
from .models import (
    BusinessInfo, ServiceCategory, ServiceItem, LaptopBrand, LaptopRepairIssue,
    NetworkPackage, ServiceBooking, ContactMessage, Testimonial, FAQ,
    PortfolioProject, ProjectImage, ProjectTechnology,
    SiteMetric, CorePillar
)

admin.site.site_header = "TechStyle Solutions Control Desk"
admin.site.site_title = "TechStyle Solutions Portal"
admin.site.index_title = "TechStyle Solutions Administration"


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Business Branding', {
            'fields': ('business_name', 'site_logo', 'announcement_banner', 'about_us_footer')
        }),
        ('Home Page Hero & CTA', {
            'fields': ('hero_title', 'hero_subtitle', 'global_cta_title', 'global_cta_text')
        }),
        ('SEO Configuration', {
            'fields': ('seo_title_suffix', 'seo_meta_description')
        }),
        ('Contact Numbers & Email', {
            'fields': ('phone_primary', 'phone_secondary', 'whatsapp_number', 'email')
        }),
        ('Location & Hours', {
            'fields': ('address', 'opening_hours_weekday', 'opening_hours_saturday', 'opening_hours_sunday')
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1
    fields = ('title', 'starting_price', 'badge_text', 'is_featured')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)
    inlines = [ServiceItemInline]


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'starting_price', 'badge_text', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'features_list')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('starting_price', 'badge_text', 'is_featured')


class LaptopRepairIssueInline(admin.TabularInline):
    model = LaptopRepairIssue
    extra = 1
    fields = ('issue_name', 'estimated_cost_min', 'estimated_cost_max', 'turnaround_time')


@admin.register(LaptopBrand)
class LaptopBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_name')
    search_fields = ('name',)
    inlines = [LaptopRepairIssueInline]


@admin.register(LaptopRepairIssue)
class LaptopRepairIssueAdmin(admin.ModelAdmin):
    list_display = ('issue_name', 'brand', 'estimated_cost_min', 'estimated_cost_max', 'turnaround_time')
    list_filter = ('brand',)
    search_fields = ('issue_name', 'description')
    list_editable = ('estimated_cost_min', 'estimated_cost_max', 'turnaround_time')


@admin.register(NetworkPackage)
class NetworkPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_audience', 'price_estimate', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('title', 'target_audience', 'features_list')
    list_editable = ('price_estimate', 'is_popular')


@admin.action(description="Mark selected tickets as Completed")
def mark_as_completed(modeladmin, request, queryset):
    queryset.update(status='completed', status_notes='Repair / Installation / Development completed successfully.')


@admin.action(description="Mark selected tickets as In Progress")
def mark_as_in_progress(modeladmin, request, queryset):
    queryset.update(status='in_progress', status_notes='Specialists currently actively servicing ticket.')


@admin.action(description="Mark selected tickets as Ready for Handoff / Deployed")
def mark_as_ready(modeladmin, request, queryset):
    queryset.update(status='ready', status_notes='Service complete. Hardware / Application ready for deployment.')


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'customer_name', 'customer_phone', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('booking_ref', 'customer_name', 'customer_phone', 'customer_email', 'details')
    list_editable = ('status',)
    readonly_fields = ('booking_ref', 'created_at', 'updated_at')
    actions = [mark_as_completed, mark_as_in_progress, mark_as_ready]
    fieldsets = (
        ('Ticket Identity', {
            'fields': ('booking_ref', 'status', 'status_notes')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Service & Issue Requirements', {
            'fields': ('service_type', 'details', 'preferred_date')
        }),
        ('System Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.action(description="Mark selected messages as Resolved")
def mark_as_resolved(modeladmin, request, queryset):
    queryset.update(is_resolved=True)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_resolved',)
    actions = [mark_as_resolved]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'service_used', 'rating', 'is_verified')
    list_filter = ('rating', 'is_verified')
    search_fields = ('client_name', 'comment')
    list_editable = ('rating', 'is_verified')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    ordering = ('category', 'order')
    list_editable = ('order',)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'is_before', 'is_after', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; border-radius: 6px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Preview"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completion_date', 'is_featured', 'order', 'cover_preview')
    list_filter = ('category', 'is_featured', 'technologies')
    search_fields = ('title', 'challenge', 'solution', 'results')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'order')
    filter_horizontal = ('technologies',)
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'slug', 'category', 'description', 'technologies')
        }),
        ('Client Story', {
            'fields': ('challenge', 'solution', 'results'),
            'classes': ('collapse',)
        }),
        ('Media & Display', {
            'fields': ('cover_image', 'completion_date', 'project_duration', 'is_featured', 'order')
        }),
    )
    ordering = ('order', '-completion_date')

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 6px;" />', obj.cover_image.url)
        return "—"
    cover_preview.short_description = "Cover"


@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_name')
    search_fields = ('name',)


@admin.register(SiteMetric)
class SiteMetricAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'order')
    list_editable = ('value', 'suffix', 'order')
    ordering = ('order',)


@admin.register(CorePillar)
class CorePillarAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')
    list_editable = ('icon_name', 'order')
    ordering = ('order',)
