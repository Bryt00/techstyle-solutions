from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests as http_requests
from decimal import Decimal

from .models import (
    ServiceCategory, ServiceItem, LaptopBrand, LaptopRepairIssue,
    NetworkPackage, ServiceBooking, ContactMessage, Testimonial, FAQ,
    PortfolioProject, SiteMetric, CorePillar,
    ShopCategory, ShopProduct, ShopOrder, OrderItem
)


# ── Page Views ──────────────────────────────────────────────────────────────

def home_view(request):
    """Home page: hero + 4 pillar cards + featured projects + testimonials + CTA."""
    categories = ServiceCategory.objects.all()
    featured_projects = PortfolioProject.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.all()[:6]
    metrics = SiteMetric.objects.all()
    pillars = CorePillar.objects.all()

    context = {
        'categories': categories,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'metrics': metrics,
        'pillars': pillars,
    }
    return render(request, 'services/home.html', context)


def services_view(request):
    """Full services catalog with category filter tabs."""
    categories = ServiceCategory.objects.all()
    services = ServiceItem.objects.select_related('category').all()

    context = {
        'categories': categories,
        'services': services,
    }
    return render(request, 'services/services.html', context)


def cctv_view(request):
    """CCTV packages showcase + project cost estimator widget."""
    return render(request, 'services/cctv.html')


def networking_view(request):
    """Networking equipment packages page."""
    network_packages = NetworkPackage.objects.all()

    context = {
        'network_packages': network_packages,
    }
    return render(request, 'services/networking.html', context)


def repairs_view(request):
    """Laptop repair cost estimator page."""
    laptop_brands = LaptopBrand.objects.all()
    laptop_issues = LaptopRepairIssue.objects.select_related('brand').all()

    context = {
        'laptop_brands': laptop_brands,
        'laptop_issues': laptop_issues,
    }
    return render(request, 'services/repairs.html', context)


def portfolio_view(request):
    """Project portfolio gallery with optional category filtering."""
    category_slug = request.GET.get('category', '')
    categories = ServiceCategory.objects.all()
    projects = PortfolioProject.objects.select_related('category').prefetch_related('technologies').all()

    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    context = {
        'categories': categories,
        'projects': projects,
        'active_category': category_slug,
    }
    return render(request, 'services/portfolio.html', context)


def portfolio_detail_view(request, slug):
    """Single project showcase with gallery, before/after, and story."""
    project = get_object_or_404(
        PortfolioProject.objects.select_related('category').prefetch_related('technologies', 'images'),
        slug=slug
    )
    gallery_images = project.images.all()
    before_images = gallery_images.filter(is_before=True)
    after_images = gallery_images.filter(is_after=True)
    regular_images = gallery_images.filter(is_before=False, is_after=False)
    related_projects = PortfolioProject.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]

    context = {
        'project': project,
        'gallery_images': regular_images,
        'before_images': before_images,
        'after_images': after_images,
        'related_projects': related_projects,
    }
    return render(request, 'services/portfolio_detail.html', context)


def contact_view(request):
    """Contact form + FAQ accordion page."""
    faqs = FAQ.objects.all()

    context = {
        'faqs': faqs,
    }
    return render(request, 'services/contact.html', context)


# ── API Endpoints ───────────────────────────────────────────────────────────

def estimate_repair_cost_api(request):
    brand_id = request.GET.get('brand_id')
    issue_id = request.GET.get('issue_id')

    issue = None
    if issue_id:
        issue = LaptopRepairIssue.objects.filter(id=issue_id).first()

    if not issue:
        return JsonResponse({'error': 'Repair issue not found'}, status=404)

    return JsonResponse({
        'issue_id': issue.id,
        'issue_name': issue.issue_name,
        'brand_name': issue.brand.name if issue.brand else "All Laptops",
        'estimated_cost_min': float(issue.estimated_cost_min),
        'estimated_cost_max': float(issue.estimated_cost_max),
        'turnaround_time': issue.turnaround_time,
        'description': issue.description
    })


@require_POST
def create_booking_api(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    customer_name = data.get('customer_name', '').strip()
    customer_phone = data.get('customer_phone', '').strip()
    customer_email = data.get('customer_email', '').strip()
    service_type = data.get('service_type', 'General Inquiry').strip()
    details = data.get('details', '').strip()
    preferred_date = data.get('preferred_date', None) or None

    if not customer_name or not customer_phone or not details:
        return JsonResponse({
            'success': False,
            'error': 'Please provide your Name, Phone Number, and Service Details.'
        }, status=400)

    booking = ServiceBooking.objects.create(
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        service_type=service_type,
        details=details,
        preferred_date=preferred_date,
        status='received',
        status_notes='Booking request logged. Our TechStyle specialists will contact you shortly to confirm schedule.'
    )

    return JsonResponse({
        'success': True,
        'booking_ref': booking.booking_ref,
        'message': f'Booking created successfully! Your Reference ID is {booking.booking_ref}.'
    })


def track_repair_api(request):
    ref = request.GET.get('ref', '').strip()
    if not ref:
        return JsonResponse({'error': 'Reference code is required'}, status=400)

    booking = ServiceBooking.objects.filter(booking_ref__iexact=ref).first()
    if not booking:
        return JsonResponse({
            'found': False,
            'message': f'No ticket found matching reference code "{ref}".'
        })

    status_steps = ['received', 'diagnostics', 'in_progress', 'testing', 'ready', 'completed']
    current_index = status_steps.index(booking.status) if booking.status in status_steps else 0
    progress_percentage = int(((current_index + 1) / len(status_steps)) * 100)

    return JsonResponse({
        'found': True,
        'booking_ref': booking.booking_ref,
        'customer_name': booking.customer_name,
        'service_type': booking.service_type,
        'status_code': booking.status,
        'status_display': booking.get_status_display(),
        'status_notes': booking.status_notes or "Ticket processed.",
        'progress_percentage': progress_percentage,
        'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': booking.updated_at.strftime('%Y-%m-%d %H:%M')
    })


@require_POST
def contact_submit_api(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    subject = data.get('subject', 'General Inquiry').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return JsonResponse({
            'success': False,
            'error': 'Please provide your Name, Email address, and Message.'
        }, status=400)

    ContactMessage.objects.create(
        name=name,
        email=email,
        phone=phone,
        subject=subject,
        message=message
    )

    return JsonResponse({
        'success': True,
        'message': 'Thank you! Your message has been received by TechStyle Solutions. We will get back to you shortly.'
    })


# ── Shop Views ──────────────────────────────────────────────────────────────

def shop_view(request):
    """Shop page with product grid, category filters, and cart."""
    category_slug = request.GET.get('category', '')
    categories = ShopCategory.objects.all()
    products = ShopProduct.objects.filter(in_stock=True).select_related('category')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'categories': categories,
        'products': products,
        'active_category': category_slug,
        'paystack_public_key': os.environ.get('PAYSTACK_PUBLIC_KEY', ''),
    }
    return render(request, 'services/shop.html', context)


@require_POST
def create_shop_order_api(request):
    """Create an order from cart items. Returns order_ref + total for Paystack payment."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data.'}, status=400)

    customer_name = data.get('customer_name', '').strip()
    customer_phone = data.get('customer_phone', '').strip()
    customer_email = data.get('customer_email', '').strip()
    delivery_address = data.get('delivery_address', '').strip()
    notes = data.get('notes', '').strip()
    cart_items = data.get('items', [])

    if not customer_name or not customer_phone or not customer_email or not delivery_address:
        return JsonResponse({
            'success': False,
            'error': 'Please provide your Name, Phone, Email, and Delivery Address.'
        }, status=400)

    if not cart_items:
        return JsonResponse({
            'success': False,
            'error': 'Your cart is empty.'
        }, status=400)

    # Create the order
    order = ShopOrder.objects.create(
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        delivery_address=delivery_address,
        notes=notes,
        status='pending_payment',
        status_notes='Order created. Awaiting payment confirmation.'
    )

    total = Decimal('0.00')
    for item in cart_items:
        product_id = item.get('product_id')
        quantity = int(item.get('quantity', 1))
        product = ShopProduct.objects.filter(id=product_id, in_stock=True).first()
        if product:
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            )
            total += product.price * quantity

    order.total_amount = total
    order.save()

    return JsonResponse({
        'success': True,
        'order_ref': order.order_ref,
        'total_amount': float(total),
        'customer_email': customer_email,
        'order_id': order.id,
    })


@csrf_exempt
@require_POST
def verify_paystack_payment_api(request):
    """Verify Paystack payment and update order status."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

    reference = data.get('reference', '').strip()
    order_id = data.get('order_id')

    if not reference or not order_id:
        return JsonResponse({'success': False, 'error': 'Missing reference or order.'}, status=400)

    # Verify with Paystack API
    paystack_secret = os.environ.get('PAYSTACK_SECRET_KEY', '')
    headers = {
        'Authorization': f'Bearer {paystack_secret}',
    }

    try:
        response = http_requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers,
            timeout=15
        )
        result = response.json()
    except Exception:
        return JsonResponse({'success': False, 'error': 'Could not verify payment.'}, status=500)

    if result.get('status') and result['data'].get('status') == 'success':
        order = ShopOrder.objects.filter(id=order_id).first()
        if order:
            order.paystack_reference = reference
            order.payment_verified = True
            order.status = 'paid'
            order.status_notes = 'Payment confirmed via Paystack. Your order is being processed.'
            order.save()
            return JsonResponse({
                'success': True,
                'order_ref': order.order_ref,
                'message': f'Payment verified! Your order reference is {order.order_ref}.'
            })

    return JsonResponse({'success': False, 'error': 'Payment verification failed.'}, status=400)
