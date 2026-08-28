import random
import string
from django.db import models
from django.utils.text import slugify
from typing import TYPE_CHECKING


def generate_booking_ref():
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=6))
    return f"TS-{code}"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="wrench")
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceItem(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="check-circle")
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=True)
    features_list = models.TextField(help_text="Enter features separated by newlines", blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    def get_features(self):
        if not self.features_list:
            return []
        return [f.strip() for f in str(self.features_list).split('\n') if f.strip()]


class LaptopBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo_name = models.CharField(max_length=50, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LaptopRepairIssue(models.Model):
    brand = models.ForeignKey(LaptopBrand, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    issue_name = models.CharField(max_length=150)
    estimated_cost_min = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_cost_max = models.DecimalField(max_digits=8, decimal_places=2)
    turnaround_time = models.CharField(max_length=50, default="Same Day (2-4 hrs)")
    description = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['issue_name']

    def __str__(self):
        brand_name = self.brand.name if self.brand else "All Brands"
        return f"[{brand_name}] {self.issue_name}"


class NetworkPackage(models.Model):
    title = models.CharField(max_length=150)
    target_audience = models.CharField(max_length=100, help_text="e.g. Home Wi-Fi, SMB Office, Enterprise")
    price_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    icon_name = models.CharField(max_length=50, default="wifi")
    features_list = models.TextField(help_text="Enter items separated by newlines")
    is_popular = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['price_estimate']

    def __str__(self):
        return self.title

    def get_features(self):
        if not self.features_list:
            return []
        return [f.strip() for f in str(self.features_list).split('\n') if f.strip()]


class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('received', 'Ticket Received'),
        ('diagnostics', 'Under Assessment / Diagnostics'),
        ('in_progress', 'Development / Installation in Progress'),
        ('testing', 'Quality Testing & QA'),
        ('ready', 'Ready / Deployed'),
        ('completed', 'Completed'),
    ]

    booking_ref = models.CharField(max_length=15, unique=True, default=generate_booking_ref)
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    service_type = models.CharField(max_length=100, help_text="e.g. Web Solutions, CCTV Installation, Networking, Laptop Repair")
    details = models.TextField(help_text="Issue description, project specs, or networking requirement")
    preferred_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    status_notes = models.TextField(blank=True, help_text="Technician progress notes shown to customer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_ref} - {self.customer_name} ({self.service_type})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, help_text="e.g. Small Business Owner, Resident, Tech Lead")
    service_used = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    is_verified = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f"{self.client_name} - {self.service_used}"


class FAQ(models.Model):
    CATEGORIES = [
        ('web', 'Web Solutions & Apps'),
        ('cctv', 'CCTV & Security Systems'),
        ('networking', 'Networking & Infrastructure'),
        ('repairs', 'Laptop & PC Repairs'),
        ('general', 'General Inquiries'),
    ]

    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class ProjectTechnology(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon_name = models.CharField(max_length=50, blank=True, help_text="Lucide icon name for visual badge")

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Project Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name


class PortfolioProject(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name="portfolio_projects")
    client_name = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    challenge = models.TextField(blank=True, help_text="Problem or challenge the client faced")
    solution = models.TextField(blank=True, help_text="How TechStyle Solutions solved it")
    results = models.TextField(blank=True, help_text="Outcomes, metrics, or impact achieved")
    cover_image = models.ImageField(upload_to='portfolio/covers/', help_text="Primary showcase image")
    technologies = models.ManyToManyField(ProjectTechnology, blank=True, related_name="projects")
    completion_date = models.DateField(null=True, blank=True)
    project_duration = models.CharField(max_length=50, blank=True, help_text="e.g. 3 Weeks, Same Day")
    is_featured = models.BooleanField(default=False, help_text="Show on home page featured strip")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    if TYPE_CHECKING:
        images: models.Manager['ProjectImage']

    objects = models.Manager()

    class Meta:
        ordering = ['order', '-completion_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_before = models.BooleanField(default=False, help_text="Mark as 'before' image for comparison")
    is_after = models.BooleanField(default=False, help_text="Mark as 'after' image for comparison")
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['order']

    def __str__(self):
        label = self.caption or f"Image {self.order}"
        if self.is_before:
            label = f"[BEFORE] {label}"
        elif self.is_after:
            label = f"[AFTER] {label}"
        return f"{self.project.title} - {label}"


class BusinessInfo(models.Model):
    business_name = models.CharField(max_length=150, default="TechStyle Solutions")
    phone_primary = models.CharField(max_length=30, default="+233 (0) 24 000 0000")
    phone_secondary = models.CharField(max_length=30, default="+233 (0) 50 000 0000", blank=True)
    whatsapp_number = models.CharField(max_length=30, default="233240000000", help_text="Number with country code for WhatsApp link e.g. 233240000000")
    email = models.EmailField(default="support@techstylesolutions.com")
    address = models.CharField(max_length=255, default="Tech Hub Street, Main Business District, Suite 4B")
    opening_hours_weekday = models.CharField(max_length=100, default="8:00 AM - 7:00 PM")
    opening_hours_saturday = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")
    opening_hours_sunday = models.CharField(max_length=100, default="Closed / Emergency Support")
    announcement_banner = models.CharField(max_length=255, default="Open Today • 8:00 AM - 7:00 PM", help_text="Text shown in top header status bar")
    facebook_url = models.URLField(blank=True, default="#")
    instagram_url = models.URLField(blank=True, default="#")
    twitter_url = models.URLField(blank=True, default="#")

    # Dynamic branding, SEO and hero content
    site_logo = models.ImageField(upload_to='branding/logo/', blank=True, null=True, help_text="Upload a custom logo to replace the default icon")
    hero_title = models.CharField(max_length=200, default="Web Apps, CCTV Systems & Network Solutions")
    hero_subtitle = models.TextField(default="From custom fullstack Django web applications and 24/7 HD CCTV security installations to enterprise network equipment sales and express hardware laptop repairs—we power your digital world.")
    about_us_footer = models.TextField(default="Your trusted partner for custom web solutions & software applications, HD CCTV security installations, network equipment sales & structured cabling, and laptop hardware repairs.")
    global_cta_title = models.CharField(max_length=150, default="Need a Custom Solution?")
    global_cta_text = models.TextField(default="Don't see exactly what you need? Our team builds custom solutions tailored to your business requirements.")
    seo_title_suffix = models.CharField(max_length=150, default="TechStyle Solutions - Web Solutions, CCTV Installations, Networking & Laptop Repairs")
    seo_meta_description = models.TextField(default="TechStyle Solutions - Custom Web Applications & Software, HD CCTV Security Installations, Sale of Enterprise Networking Equipment, and Express Laptop Repairs.")

    objects = models.Manager()

    class Meta:
        verbose_name = "Business Info & Contact Details"
        verbose_name_plural = "Business Info & Contact Details"

    def __str__(self):
        return self.business_name


class SiteMetric(models.Model):
    value = models.IntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True, default="+")
    label = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class CorePillar(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="check-circle")
    button_text = models.CharField(max_length=50, default="Explore")
    button_link = models.CharField(max_length=200, help_text="URL or path, e.g. /services/")
    features_list = models.TextField(help_text="Enter features separated by newlines", blank=True)
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['order']
        verbose_name = "Core Service"
        verbose_name_plural = "Core Services"

    def __str__(self):
        return self.title

    def get_features(self):
        if not self.features_list:
            return []
        return [f.strip() for f in str(self.features_list).split('\n') if f.strip()]


# ── Shop / E-Commerce Models ─────────────────────────────────────────────────

class ShopCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon_name = models.CharField(max_length=50, default="package", help_text="Lucide icon name")
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Shop Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ShopProduct(models.Model):
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='shop/products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Selling price in GHS")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price (shown as strike-through if set)")
    badge_text = models.CharField(max_length=50, blank=True, help_text="e.g. Hot Deal, New Arrival, Limited Stock")
    in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured/highlighted section")
    specs_list = models.TextField(blank=True, help_text="Key specs separated by newlines")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.name} — GHS {self.price}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_specs(self):
        if not self.specs_list:
            return []
        return [s.strip() for s in str(self.specs_list).split('\n') if s.strip()]

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


def generate_order_ref():
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=6))
    return f"TS-{code}"


class ShopOrder(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Payment Received'),
        ('confirmed', 'Order Confirmed'),
        ('processing', 'Processing / Packing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_ref = models.CharField(max_length=15, unique=True, default=generate_order_ref)
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    delivery_address = models.TextField(help_text="Full delivery address")
    notes = models.TextField(blank=True, help_text="Special instructions or notes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    status_notes = models.TextField(blank=True, help_text="Internal notes / updates shown to customer")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paystack_reference = models.CharField(max_length=100, blank=True, help_text="Paystack transaction reference")
    payment_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_ref} — {self.customer_name} (GHS {self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(ShopOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ShopProduct, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_name = models.CharField(max_length=200, help_text="Snapshot of product name at time of order")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price
