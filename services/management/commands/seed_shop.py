import os
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files import File
from services.models import ShopCategory, ShopProduct


class Command(BaseCommand):
    help = "Seed shop categories and initial products with generated realistic product graphics."

    def handle(self, *args, **options):
        style_success = getattr(self.style, 'SUCCESS', str)
        self.stdout.write(style_success("Seeding TechStyle Shop categories & products..."))

        # Create media dir for shop products if it doesn't exist
        media_shop_dir = os.path.join("media", "shop", "products")
        os.makedirs(media_shop_dir, exist_ok=True)

        # 1. Shop Categories
        cat_laptops, _ = ShopCategory.objects.get_or_create(
            slug="laptops-computers",
            defaults={"name": "Laptops & Computers", "icon_name": "laptop", "order": 1}
        )
        cat_cctv, _ = ShopCategory.objects.get_or_create(
            slug="cctv-security",
            defaults={"name": "CCTV & Security", "icon_name": "video", "order": 2}
        )
        cat_net, _ = ShopCategory.objects.get_or_create(
            slug="networking-gear",
            defaults={"name": "Networking Gear", "icon_name": "wifi", "order": 3}
        )
        cat_acc, _ = ShopCategory.objects.get_or_create(
            slug="accessories-storage",
            defaults={"name": "Accessories & Storage", "icon_name": "hard-drive", "order": 4}
        )

        # Products dataset
        products_data = [
            # Laptops
            {
                "category": cat_laptops,
                "name": "Dell XPS 15 Touchscreen Laptop",
                "slug": "dell-xps-15-touchscreen",
                "description": "Premium workstation laptop for developers, engineers, and creators. Features sleek aluminum chassis and vibrant OLED touch display.",
                "price": 18500.00,
                "old_price": 21000.00,
                "badge_text": "Hot Deal",
                "in_stock": True,
                "is_featured": True,
                "specs_list": "Intel Core i9 13th Gen\n32GB DDR5 RAM\n1TB M.2 NVMe SSD\nNVIDIA RTX 4060 8GB\n15.6\" 3.5K OLED Touch Display",
                "color": (31, 39, 35),  # Forest Dark
                "accent": (200, 90, 50), # Terracotta
                "type_text": "DELL XPS 15"
            },
            {
                "category": cat_laptops,
                "name": "MacBook Pro 16\" M3 Pro",
                "slug": "macbook-pro-16-m3-pro",
                "description": "Ultimate pro laptop for software development, video editing, and heavy multitasking. Space Black finish.",
                "price": 28000.00,
                "old_price": 30500.00,
                "badge_text": "Featured",
                "in_stock": True,
                "is_featured": True,
                "specs_list": "Apple M3 Pro chip (12-core CPU, 18-core GPU)\n18GB Unified Memory\n512GB Superfast SSD\nLiquid Retina XDR Display\nUp to 22 Hours Battery Life",
                "color": (20, 24, 28),
                "accent": (230, 161, 92),
                "type_text": "MACBOOK PRO M3"
            },
            {
                "category": cat_laptops,
                "name": "HP Spectre x360 Convertible 2-in-1",
                "slug": "hp-spectre-x360-convertible",
                "description": "Versatile 360-degree flip laptop with stunning OLED touch display and all-day battery life.",
                "price": 14500.00,
                "old_price": 16000.00,
                "badge_text": "New Arrival",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "Intel Core Ultra 7\n16GB LPDDR5X RAM\n1TB PCIe Gen4 SSD\n14\" 2.8K OLED Touch Screen\nIncludes Stylus Pen & Sleeve",
                "color": (45, 55, 50),
                "accent": (200, 90, 50),
                "type_text": "HP SPECTRE X360"
            },

            # CCTV & Security
            {
                "category": cat_cctv,
                "name": "Dahua 8-Channel 4K HD Outdoor CCTV Camera Kit",
                "slug": "dahua-8-channel-4k-cctv-kit",
                "description": "Complete 8-camera surveillance package suitable for commercial buildings, stores, and residential compounds.",
                "price": 4800.00,
                "old_price": 5500.00,
                "badge_text": "Best Seller",
                "in_stock": True,
                "is_featured": True,
                "specs_list": "8x 4K (8MP) Ultra HD Bullet Cameras\n8-Channel DVR with 2TB Hard Drive\nSmart Motion Detection & Infrared Night Vision\nMobile App Remote View (iOS/Android)",
                "color": (31, 39, 35),
                "accent": (230, 161, 92),
                "type_text": "DAHUA 8-CAM 4K KIT"
            },
            {
                "category": cat_cctv,
                "name": "Hikvision 4-Camera Wireless Smart IP CCTV Kit",
                "slug": "hikvision-4-camera-wireless-ip-kit",
                "description": "Wireless security camera system with no cable clutter. Easy plug-and-play installation with instant phone alerts.",
                "price": 3200.00,
                "old_price": 3700.00,
                "badge_text": "Hot Deal",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "4x 4MP Full HD Wi-Fi IP Cameras\n4-Channel Wireless NVR + 1TB Storage\n2-Way Audio Intercom & Siren\nIP66 Weatherproof Aluminum Casing",
                "color": (40, 50, 45),
                "accent": (200, 90, 50),
                "type_text": "HIKVISION 4-CAM IP"
            },
            {
                "category": cat_cctv,
                "name": "Eufy 2K Wireless Video Doorbell & Chime",
                "slug": "eufy-2k-wireless-video-doorbell",
                "description": "Smart doorbell camera with crystal-clear 2K resolution, two-way audio, and local secure storage.",
                "price": 1450.00,
                "old_price": 1700.00,
                "badge_text": "Popular",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "2K HD Clarity with HDR\nNo Monthly Subscription Fees\nAI Human Detection\nDual Power Options (Battery / Hardwired)",
                "color": (25, 32, 28),
                "accent": (230, 161, 92),
                "type_text": "EUFY 2K DOORBELL"
            },

            # Networking Gear
            {
                "category": cat_net,
                "name": "Ubiquiti UniFi6 Long-Range Access Point (Wi-Fi 6)",
                "slug": "ubiquiti-unifi6-long-range-ap",
                "description": "High-performance ceiling-mounted access point for enterprise offices, co-working spaces, and multi-story homes.",
                "price": 1850.00,
                "old_price": 2100.00,
                "badge_text": "Top Rated",
                "in_stock": True,
                "is_featured": True,
                "specs_list": "Wi-Fi 6 High-Efficiency 4x4 MIMO\nUp to 3.0 Gbps Aggregate Throughput\n300+ Concurrent Client Support\nPoE Powered (Power over Ethernet)",
                "color": (31, 39, 35),
                "accent": (200, 90, 50),
                "type_text": "UNIFI6 LR AP"
            },
            {
                "category": cat_net,
                "name": "MikroTik Cloud Router Switch 24-Port Gigabit",
                "slug": "mikrotik-crs-24-port-gigabit-switch",
                "description": "Managed Layer 3 switch with dual SFP+ 10Gbps ports. Perfect core switch for business networks.",
                "price": 3200.00,
                "old_price": 3600.00,
                "badge_text": "Enterprise",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "24x Gigabit Ethernet Ports\n2x 10G SFP+ Fiber Ports\nDual Boot (RouterOS / SwOS)\n1U Rackmount Enclosure",
                "color": (22, 28, 25),
                "accent": (230, 161, 92),
                "type_text": "MIKROTIK 24P SWITCH"
            },
            {
                "category": cat_net,
                "name": "TP-Link Omada AX3000 Gigabit VPN Router",
                "slug": "tp-link-omada-ax3000-vpn-router",
                "description": "Secure business router supporting multi-ISP failover and encrypted remote office connections.",
                "price": 1100.00,
                "old_price": 1300.00,
                "badge_text": "In Stock",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "Multi-WAN Load Balancing\nHardware VPN Engine (IPsec/PPTP/L2TP)\nOmada SDN Centralized Management\nGigabit Ethernet Ports",
                "color": (45, 55, 50),
                "accent": (200, 90, 50),
                "type_text": "TP-LINK OMADA ROUTER"
            },

            # Accessories & Storage
            {
                "category": cat_acc,
                "name": "Kingston 1TB NVMe M.2 PCIe 4.0 SSD",
                "slug": "kingston-1tb-nvme-m2-ssd",
                "description": "Upgrade your laptop or desktop speed with high-efficiency M.2 NVMe solid-state storage.",
                "price": 850.00,
                "old_price": 1000.00,
                "badge_text": "Super Speed",
                "in_stock": True,
                "is_featured": True,
                "specs_list": "Read Speed up to 3,500 MB/s\nWrite Speed up to 2,100 MB/s\nM.2 2280 Form Factor\n5-Year Limited Warranty",
                "color": (31, 39, 35),
                "accent": (230, 161, 92),
                "type_text": "KINGSTON 1TB NVME"
            },
            {
                "category": cat_acc,
                "name": "Logitech MX Master 3S Wireless Performance Mouse",
                "slug": "logitech-mx-master-3s-mouse",
                "description": "Ergonomic master mouse designed for coders, designers, and power users. Seamless multi-device switching.",
                "price": 1200.00,
                "old_price": 1400.00,
                "badge_text": "Hot Deal",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "8000 DPI Any-Surface Tracking\nQuiet Click Switches (90% Noise Reduction)\nMagSpeed Electromagnetic Scroll Wheel\nUSB-C Fast Charging (70-Day Battery)",
                "color": (28, 35, 32),
                "accent": (200, 90, 50),
                "type_text": "LOGITECH MX MASTER 3S"
            },
            {
                "category": cat_acc,
                "name": "Anker PowerConf 8-in-1 USB-C Hub Adapter",
                "slug": "anker-powerconf-8-in-1-usb-c-hub",
                "description": "Premium multiport adapter for laptops and MacBooks. Turn one USB-C port into a full workstation hub.",
                "price": 650.00,
                "old_price": 780.00,
                "badge_text": "Essential",
                "in_stock": True,
                "is_featured": False,
                "specs_list": "4K 60Hz HDMI Output\n100W Power Delivery Pass-Through\n1Gbps Ethernet Port\nSD / microSD Card Readers + USB 3.0 Ports",
                "color": (40, 48, 44),
                "accent": (230, 161, 92),
                "type_text": "ANKER USB-C HUB"
            }
        ]

        def create_product_graphic(filename, bg_color, accent_color, text_title, category_name):
            width, height = 600, 600
            img = Image.new("RGB", (width, height), bg_color)
            draw = ImageDraw.Draw(img)

            # Draw background geometric design
            draw.rectangle([0, 0, width, height], fill=bg_color)
            
            # Subtle decorative circle
            draw.ellipse([width*0.2, height*0.15, width*0.8, height*0.75], outline=accent_color, width=4)
            draw.ellipse([width*0.25, height*0.2, width*0.75, height*0.7], fill=(*accent_color, 40) if len(accent_color)==4 else accent_color)

            # Center card box
            card_rect = [width*0.1, height*0.35, width*0.9, height*0.85]
            draw.rounded_rectangle(card_rect, radius=20, fill=(255, 255, 255))

            # Header brand bar
            draw.rounded_rectangle([width*0.1, height*0.35, width*0.9, height*0.48], radius=15, fill=accent_color)

            # Add Text inside card using default font
            draw.text((width*0.15, height*0.39), "TECHSTYLE SHOP", fill=(255, 255, 255))
            draw.text((width*0.15, height*0.53), category_name.upper(), fill=(120, 120, 120))
            draw.text((width*0.15, height*0.62), text_title, fill=(31, 39, 35))
            draw.text((width*0.15, height*0.73), "GENUINE PRODUCT • OFFICIAL WARRANTY", fill=accent_color)

            filepath = os.path.join(media_shop_dir, filename)
            img.save(filepath, "PNG")
            return filepath

        created_count = 0
        for p in products_data:
            cat = p["category"]
            cat_name = getattr(cat, "name", str(cat))
            img_filename = f"{p['slug']}.png"
            img_path = create_product_graphic(
                img_filename,
                p["color"],
                p["accent"],
                p["type_text"],
                cat_name
            )

            product, created = ShopProduct.objects.get_or_create(
                slug=p["slug"],
                defaults={
                    "category": p["category"],
                    "name": p["name"],
                    "description": p["description"],
                    "price": p["price"],
                    "old_price": p["old_price"],
                    "badge_text": p["badge_text"],
                    "in_stock": p["in_stock"],
                    "is_featured": p["is_featured"],
                    "specs_list": p["specs_list"],
                }
            )

            # Assign image field
            with open(img_path, 'rb') as f:
                product.image.save(img_filename, File(f), save=True)

            created_count += 1
            self.stdout.write(style_success(f"  ✓ Product: {product.name} (GHS {product.price})"))

        self.stdout.write(style_success(f"\nSuccessfully seeded {created_count} products across {ShopCategory.objects.count()} categories!"))
