from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import (
    BusinessInfo, ServiceCategory, ServiceItem, LaptopBrand, LaptopRepairIssue,
    NetworkPackage, ServiceBooking, Testimonial, FAQ,
    PortfolioProject, ProjectImage, ProjectTechnology,
    SiteMetric, CorePillar
)


class Command(BaseCommand):
    help = "Seed database with initial TechStyle Solutions services, web apps, CCTV kits, network packages, repair issues, and admin superuser."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting TechStyle Solutions database seeding..."))

        # 0. Admin Superuser & Business Info
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@techstylesolutions.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Created Admin Superuser: username='admin', password='admin123'"))

        BusinessInfo.objects.get_or_create(
            id=1,
            defaults={
                "business_name": "TechStyle Solutions",
                "phone_primary": "+233 (0) 24 000 0000",
                "phone_secondary": "+233 (0) 50 000 0000",
                "whatsapp_number": "233240000000",
                "email": "support@techstylesolutions.com",
                "address": "Tech Hub Street, Main Business District, Suite 4B",
                "opening_hours_weekday": "8:00 AM - 7:00 PM",
                "opening_hours_saturday": "9:00 AM - 6:00 PM",
                "opening_hours_sunday": "Closed / Emergency Support",
                "announcement_banner": "Open Today • 8:00 AM - 7:00 PM",
                "hero_title": "Web Apps, CCTV Systems & Network Solutions",
                "hero_subtitle": "From custom fullstack Django web applications and 24/7 HD CCTV security installations to enterprise network equipment sales and express hardware laptop repairs—we power your digital world.",
                "about_us_footer": "Your trusted partner for custom web solutions & software applications, HD CCTV security installations, network equipment sales & structured cabling, and laptop hardware repairs.",
                "global_cta_title": "Need a Custom Solution?",
                "global_cta_text": "Don't see exactly what you need? Our team builds custom solutions tailored to your business requirements.",
                "seo_title_suffix": "TechStyle Solutions | Web Apps, CCTV Systems, Networking & Laptop Repairs",
                "seo_meta_description": "TechStyle Solutions - Custom Web Applications & Software, HD CCTV Security Installations, Sale of Enterprise Networking Equipment, and Express Laptop Repairs.",
            }
        )

        # 1. Categories
        cat_web, _ = ServiceCategory.objects.get_or_create(
            slug="web-solutions",
            defaults={
                "name": "Web Solutions & Software",
                "description": "Fullstack web applications, Django backends, React interfaces, custom corporate portals, e-commerce, and cloud backend architecture.",
                "icon_name": "globe",
                "order": 1,
            }
        )

        cat_cctv, _ = ServiceCategory.objects.get_or_create(
            slug="cctv-security",
            defaults={
                "name": "CCTV & Security Systems",
                "description": "HD & IP security camera installations, NVR/DVR storage setup, motion alerts, and 24/7 smartphone live monitoring.",
                "icon_name": "video",
                "order": 2,
            }
        )

        cat_net, _ = ServiceCategory.objects.get_or_create(
            slug="networking",
            defaults={
                "name": "Networking & Infrastructure",
                "description": "Sales of enterprise routers & managed switches, structured Cat6 cabling, fiber optic accessories, and seamless mesh Wi-Fi.",
                "icon_name": "network",
                "order": 3,
            }
        )

        cat_repair, _ = ServiceCategory.objects.get_or_create(
            slug="repairs",
            defaults={
                "name": "Laptop & PC Repairs",
                "description": "Expert hardware component repair, screen replacements, NVMe SSD speed upgrades, liquid spill restoration, and OS setup.",
                "icon_name": "wrench",
                "order": 4,
            }
        )

        # 2. Service Items
        services_data = [
            # Web Solutions
            {
                "category": cat_web,
                "title": "Custom Web Application Development",
                "slug": "custom-web-application",
                "subtitle": "Tailored Django & React web applications designed for your business needs",
                "description": "Complete web app creation with database modeling, REST API endpoints, custom user role management, and responsive frontends.",
                "icon_name": "code",
                "starting_price": 1500.00,
                "badge_text": "Most Requested",
                "features_list": "Django / React Fullstack Architecture\nDatabase & Admin Desk Setup\nResponsive Mobile-First Interface\nSecure Authentication & Role Access"
            },
            {
                "category": cat_web,
                "title": "E-Commerce & Online Store Platform",
                "slug": "ecommerce-platform",
                "subtitle": "Sell products online with mobile money & credit card payment gateways",
                "description": "High-converting online store with product inventory, order tracking, SMS notifications, and payment checkout integration.",
                "icon_name": "shopping-cart",
                "starting_price": 2500.00,
                "badge_text": "High ROI",
                "features_list": "Integrated Payment Gateway (Paystack/Hubtel)\nInventory & Product Catalog\nOrder Management & SMS Alerts\nSEO & Analytics Setup"
            },
            {
                "category": cat_web,
                "title": "Corporate Website & UI/UX Redesign",
                "slug": "corporate-website-redesign",
                "subtitle": "Transform your brand with a sleek, ultra-fast modern web application",
                "description": "Modern web redesign utilizing high-performance CSS, smooth micro-animations, fast load times, and custom client inquiry desk.",
                "icon_name": "layout",
                "starting_price": 1200.00,
                "badge_text": "Instant Impact",
                "features_list": "Ultra-Fast Page Load Performance\nModern Glassmorphic & Modern Aesthetic\nInteractive Contact & Inquiry Modals\nFull Mobile Responsiveness"
            },

            # CCTV Systems
            {
                "category": cat_cctv,
                "title": "4-Camera HD Night-Vision CCTV Kit",
                "slug": "4-cam-hd-cctv-kit",
                "subtitle": "Complete security surveillance package for small offices and homes",
                "description": "Full HD 1080p indoor/outdoor weather-resistant cameras with infrared night vision, 1TB DVR storage, and live mobile monitoring app.",
                "icon_name": "video",
                "starting_price": 2200.00,
                "badge_text": "Best Seller",
                "features_list": "4x Full HD 1080p Night-Vision Cameras\n4-Channel DVR + 1TB Hard Drive Storage\nSmartphone Remote Live Viewing\nWall Trunking & Power Installation Included"
            },
            {
                "category": cat_cctv,
                "title": "8-Camera 4K IP PoE Security System",
                "slug": "8-cam-4k-ip-cctv",
                "subtitle": "High-definition PoE surveillance system for commercial compounds & stores",
                "description": "Ultra HD 4K IP cameras with smart AI human detection, 2TB NVR recording, crystal-clear ColorVu night vision, and instant motion notifications.",
                "icon_name": "shield-check",
                "starting_price": 4800.00,
                "badge_text": "AI Detection",
                "features_list": "8x 4K IP Cameras (PoE & ColorVu Night)\n8-Channel NVR + 2TB Surveillance Hard Drive\nAI Human & Vehicle Motion Filtering\nRemote App Access & Motion Push Alerts"
            },

            # Networking
            {
                "category": cat_net,
                "title": "Sale of Enterprise Routers & Switches",
                "slug": "router-switch-sales",
                "subtitle": "Cisco, MikroTik, Ubiquiti UniFi, and TP-Link Omada hardware",
                "description": "Direct sales of gigabit managed switches, load balancing routers, PoE injectors, and outdoor wireless access point hardware.",
                "icon_name": "cpu",
                "starting_price": 300.00,
                "badge_text": "Genuine Gear",
                "features_list": "Authorized Cisco, MikroTik & Ubiquiti Hardware\nWarranty & Configuration Support\nGigabit Speed & PoE Hardware\nRackmount & Desktop Form Factors"
            },
            {
                "category": cat_net,
                "title": "Structured Cat6 Cabling & Patch Panels",
                "slug": "structured-cabling",
                "subtitle": "Neat, certified Gigabit ethernet drops for offices and multi-floor buildings",
                "description": "High-performance ethernet network installation complete with patch panels, cable trunking, labeling, and speed certification tests.",
                "icon_name": "network",
                "starting_price": 150.00,
                "badge_text": "Gigabit Rated",
                "features_list": "Cat6/Cat6A Shielded Cabling\nPatch Panel Termination & Cable Management\nSpeed & Continuity Testing\nWall Outlet Jack Installation"
            },

            # Laptop Repairs
            {
                "category": cat_repair,
                "title": "Laptop Screen Replacement",
                "slug": "screen-replacement",
                "subtitle": "Original HD, FHD & 4K IPS display panel replacement",
                "description": "Quick glass and screen replacements for MacBook, Dell, HP, Lenovo, and ASUS. Same-day turnaround available with full warranty.",
                "icon_name": "monitor",
                "starting_price": 250.00,
                "badge_text": "Same-Day Service",
                "features_list": "Genuine Grade A Displays\nClean Bezel Installation\n6-Month Screen Warranty\nFree Anti-Glare Screen Protector"
            },
            {
                "category": cat_repair,
                "title": "NVMe SSD Upgrade & RAM Boost",
                "slug": "ssd-ram-upgrade",
                "subtitle": "Make your slow laptop up to 10x faster in 1 hour",
                "description": "Upgrade old hard drives to ultra-fast M.2 NVMe SSDs with complete OS cloning and data retention guaranteed.",
                "icon_name": "zap",
                "starting_price": 120.00,
                "badge_text": "Instant Speed Up",
                "features_list": "Fast M.2 NVMe / SATA SSD Installation\nComplete OS & Data Migration\nThermal Paste Renewal & Dust Cleaning\nRAM Expansion up to 32GB/64GB"
            }
        ]

        for s in services_data:
            ServiceItem.objects.get_or_create(slug=s["slug"], defaults=s)

        # 3. Laptop Brands
        brands = ["Apple (MacBook Pro/Air)", "Dell (XPS/Latitude/Inspiron)", "HP (Spectre/Envy/Pavilion)", "Lenovo (ThinkPad/IdeaPad)", "ASUS (ROG/ZenBook)", "Acer"]
        brand_objs = {}
        for b in brands:
            obj, _ = LaptopBrand.objects.get_or_create(name=b)
            brand_objs[b] = obj

        # 4. Laptop Repair Issues
        issues_data = [
            {"brand": brand_objs["Apple (MacBook Pro/Air)"], "issue_name": "MacBook Display / Retina Glass Replacement", "estimated_cost_min": 450, "estimated_cost_max": 950, "turnaround_time": "Same Day (2-4 hrs)", "description": "Original Retina display panel replacement for M1, M2, M3 and Intel MacBooks."},
            {"brand": brand_objs["Apple (MacBook Pro/Air)"], "issue_name": "MacBook Battery Replacement & Thermal Service", "estimated_cost_min": 250, "estimated_cost_max": 450, "turnaround_time": "1-2 Hours", "description": "Genuine high-health battery swap with system diagnostics and dust cleaning."},
            {"brand": brand_objs["Dell (XPS/Latitude/Inspiron)"], "issue_name": "Dell FHD/4K Touch Display Replacement", "estimated_cost_min": 300, "estimated_cost_max": 650, "turnaround_time": "Same Day", "description": "Replacement for cracked, flickering, or line-filled displays."},
            {"brand": brand_objs["Dell (XPS/Latitude/Inspiron)"], "issue_name": "No Power / Charging Port & Motherboard Repair", "estimated_cost_min": 200, "estimated_cost_max": 450, "turnaround_time": "24 Hours", "description": "Fix for laptops failing to turn on, power jack replacements, and short circuits."},
            {"brand": brand_objs["HP (Spectre/Envy/Pavilion)"], "issue_name": "HP Battery & Hinge Replacement", "estimated_cost_min": 180, "estimated_cost_max": 350, "turnaround_time": "2 Hours", "description": "Fix broken screen hinges, chassis cracks, and worn-out batteries."},
            {"brand": brand_objs["Lenovo (ThinkPad/IdeaPad)"], "issue_name": "Keyboard & Trackpad Replacement", "estimated_cost_min": 120, "estimated_cost_max": 250, "turnaround_time": "1-2 Hours", "description": "Spill-damaged or sticky key replacements for ThinkPad and IdeaPad models."},
            {"brand": None, "issue_name": "512GB / 1TB NVMe High-Speed SSD Upgrade + OS Setup", "estimated_cost_min": 220, "estimated_cost_max": 450, "turnaround_time": "1 Hour Express", "description": "Includes cloning current drive or fresh Windows 11 / macOS install."},
            {"brand": None, "issue_name": "Liquid / Coffee Spill Decontamination", "estimated_cost_min": 150, "estimated_cost_max": 380, "turnaround_time": "24-48 Hours", "description": "Chemical bath wash for corroded logic boards, dry-out, and micro-soldering trace fixes."}
        ]

        for issue in issues_data:
            LaptopRepairIssue.objects.get_or_create(
                issue_name=issue["issue_name"],
                brand=issue["brand"],
                defaults=issue
            )

        # 5. Network Packages
        packages = [
            {
                "title": "Home Wi-Fi Mesh Starter",
                "target_audience": "Apartments & 2-3 Bedroom Homes",
                "price_estimate": 350.00,
                "icon_name": "wifi",
                "features_list": "2 Dual-Band Wi-Fi Mesh Access Points\nEliminates Dead Zones in Bedrooms & Balcony\nGuest Wi-Fi Setup\nNeat Mounting & Cabling",
                "is_popular": False
            },
            {
                "title": "Small Business Office Network",
                "target_audience": "Offices with 5-15 Workstations",
                "price_estimate": 750.00,
                "icon_name": "network",
                "features_list": "Gigabit 16-Port Managed Switch\nDual High-Speed Access Points (UniFi/Omada)\nGigabit Cat6 Network Outlets at Desks\nPatch Panel Rack Integration & Cable Labeling",
                "is_popular": True
            },
            {
                "title": "Enterprise Server & Security Pro",
                "target_audience": "Corporate Offices & Multi-Story Outlets",
                "price_estimate": 1650.00,
                "icon_name": "server",
                "features_list": "Rackmount Server Cabinet Installation\nMikroTik/UniFi Firewall & Load Balancer Router\n48-Port PoE Gigabit Switch + UPS Backup\nIntegrated CCTV & Wi-Fi VLAN Isolation",
                "is_popular": False
            }
        ]

        for pkg in packages:
            NetworkPackage.objects.get_or_create(title=pkg["title"], defaults=pkg)

        # 6. Testimonials
        testimonials = [
            {
                "client_name": "Daniel K. Mensah",
                "client_role": "Managing Director, Apex Logistics",
                "service_used": "Web Application & Office Cabling",
                "rating": 5,
                "comment": "TechStyle Solutions built our custom logistics portal and overhauled our office cabling. The web interface is ultra-fast, and internet drops are rock solid across all floors.",
                "is_verified": True
            },
            {
                "client_name": "Abena Osei",
                "client_role": "Hotel General Manager",
                "service_used": "8-Camera 4K IP CCTV Installation",
                "rating": 5,
                "comment": "The 8-camera CCTV installation was executed flawlessly. Image quality is crisp even at night, and we monitor live footage right from our smartphones.",
                "is_verified": True
            },
            {
                "client_name": "Kwame Techie",
                "client_role": "Software Developer & Freelancer",
                "service_used": "MacBook Pro Screen & Battery Swap",
                "rating": 5,
                "comment": "My MacBook screen cracked right before a big client presentation. TechStyle replaced it with an original Retina display in under 3 hours! Outstanding service.",
                "is_verified": True
            }
        ]

        for t in testimonials:
            Testimonial.objects.get_or_create(client_name=t["client_name"], defaults=t)

        # 7. FAQs
        faqs = [
            {
                "question": "What technologies do you use for custom Web Applications?",
                "answer": "We build scalable web apps using Django (Python backend) combined with modern JavaScript (React / Next.js), clean Tailwind CSS styling, RESTful APIs, and secure database architectures.",
                "category": "web",
                "order": 1
            },
            {
                "question": "Can I view my CCTV cameras remotely on my phone?",
                "answer": "Yes! All our CCTV kits include mobile app configuration for iOS and Android. You can view live video streams, playback recordings, and receive motion alert notifications anytime, anywhere.",
                "category": "cctv",
                "order": 2
            },
            {
                "question": "Do you sell networking hardware directly?",
                "answer": "Absolustely. We sell genuine enterprise routers (MikroTik, Cisco, Ubiquiti), PoE switches, patch panels, Cat6 cabling, and Wi-Fi mesh access points.",
                "category": "networking",
                "order": 3
            },
            {
                "question": "How long does a typical laptop repair take?",
                "answer": "Standard repairs such as screen replacements, SSD speed upgrades, battery swaps, and keyboards are completed on the same day within 1 to 4 hours.",
                "category": "repairs",
                "order": 4
            }
        ]

        for f in faqs:
            FAQ.objects.get_or_create(question=f["question"], defaults=f)

        # 8. Sample Bookings for Live Repair & Project Status Tracking
        sample_bookings = [
            {
                "booking_ref": "TS-782194",
                "customer_name": "Grace Addo",
                "customer_phone": "+233 24 555 0192",
                "customer_email": "grace.addo@example.com",
                "service_type": "Web Application Development",
                "details": "Custom Django & React Client Portal with Authentication",
                "status": "in_progress",
                "status_notes": "Backend REST APIs complete. Frontend UI components & dashboard rendering currently in progress.",
            },
            {
                "booking_ref": "TS-319402",
                "customer_name": "Kofi Ampofo",
                "customer_phone": "+233 50 123 4567",
                "customer_email": "kofi.amp@example.com",
                "service_type": "CCTV Installation",
                "details": "8-Camera 4K IP System Installation for Commercial Store",
                "status": "ready",
                "status_notes": "All 8 cameras mounted, cabling terminated, and NVR mobile live stream verified. Ready for client handoff.",
            }
        ]

        for sb in sample_bookings:
            ServiceBooking.objects.get_or_create(booking_ref=sb["booking_ref"], defaults=sb)

        # 9. Portfolio Technologies
        techs = [
            ("Django", "layers"),
            ("React", "code"),
            ("Tailwind CSS", "palette"),
            ("Hikvision 4K", "video"),
            ("Ubiquiti UniFi", "wifi"),
            ("Cisco", "network"),
            ("NVMe SSD", "zap")
        ]
        tech_objs = {}
        for t_name, t_icon in techs:
            obj, _ = ProjectTechnology.objects.get_or_create(name=t_name, defaults={"icon_name": t_icon})
            tech_objs[t_name] = obj

        # 10. Portfolio Projects
        portfolio_data = [
            {
                "title": "Quantum Data Analytics Portal",
                "category": cat_web,
                "client_name": "Quantum Financial Services",
                "description": "A high-performance enterprise data analytics dashboard built with Django and React, processing millions of rows daily.",
                "challenge": "Client was using slow spreadsheet macros that took hours to generate daily financial reports.",
                "solution": "We architected a custom Django REST API backend coupled with a highly responsive React frontend with interactive data visualization.",
                "results": "Report generation time reduced from 4 hours to 5 seconds. User adoption increased by 300%.",
                "cover_image": "portfolio/covers/web_app.png",
                "project_duration": "12 Weeks",
                "completion_date": "2026-03-15",
                "is_featured": True,
                "order": 1,
                "technologies": [tech_objs["Django"], tech_objs["React"], tech_objs["Tailwind CSS"]]
            },
            {
                "title": "Apex Commercial Warehouse Security",
                "category": cat_cctv,
                "client_name": "Apex Logistics HQ",
                "description": "Deployment of a 32-camera 4K IP security network across a 50,000 sq ft logistics warehouse.",
                "challenge": "Existing analog cameras were blurry at night, leading to undocumented inventory shrinkage.",
                "solution": "Installed Hikvision 4K ColorVu cameras with smart AI motion filtering and a 64-channel NVR with 16TB raid storage.",
                "results": "Inventory shrinkage reduced to 0%. Nighttime incidents now captured in full color.",
                "cover_image": "portfolio/covers/cctv.png",
                "project_duration": "2 Weeks",
                "completion_date": "2026-05-10",
                "is_featured": True,
                "order": 2,
                "technologies": [tech_objs["Hikvision 4K"], tech_objs["Cisco"]]
            },
            {
                "title": "TechHub Co-Working Network Core",
                "category": cat_net,
                "client_name": "TechHub Spaces",
                "description": "Complete gigabit network infrastructure design and installation for a 4-story co-working space.",
                "challenge": "Frequent Wi-Fi drops and slow speeds during peak hours with 200+ concurrent users.",
                "solution": "Deployed a Ubiquiti UniFi enterprise mesh network, 10Gbps fiber backbone, and robust Cisco managed switches.",
                "results": "Symmetrical gigabit speeds for all tenants with zero reported dropouts in the last 6 months.",
                "cover_image": "portfolio/covers/network.png",
                "project_duration": "4 Weeks",
                "completion_date": "2026-06-22",
                "is_featured": True,
                "order": 3,
                "technologies": [tech_objs["Ubiquiti UniFi"], tech_objs["Cisco"]]
            },
            {
                "title": "MacBook Fleet SSD Turbo Upgrade",
                "category": cat_repair,
                "client_name": "Creative Agency Inc.",
                "description": "Upgraded a fleet of 15 designer MacBooks to high-speed NVMe SSDs to improve video rendering times.",
                "challenge": "Video editors were facing extreme lag while scrubbing 4K footage on older mechanical drives.",
                "solution": "Migrated all data safely to 2TB NVMe M.2 SSDs and performed deep thermal cleaning.",
                "results": "Rendering speeds increased by 400%, extending the lifespan of the fleet by 3-4 years.",
                "cover_image": "portfolio/covers/repair.png",
                "project_duration": "3 Days",
                "completion_date": "2026-07-05",
                "is_featured": False,
                "order": 4,
                "technologies": [tech_objs["NVMe SSD"]]
            }
        ]

        for p_data in portfolio_data:
            techs = p_data.pop("technologies")
            proj, _ = PortfolioProject.objects.get_or_create(
                title=p_data["title"],
                defaults=p_data
            )
            if techs and isinstance(techs, list):
                proj.technologies.set(techs)

        # 9. Site Metrics
        SiteMetric.objects.get_or_create(label="Web Applications", defaults={"value": 250, "suffix": "+", "order": 1})
        SiteMetric.objects.get_or_create(label="CCTV Cameras", defaults={"value": 850, "suffix": "+", "order": 2})
        SiteMetric.objects.get_or_create(label="Network Drops", defaults={"value": 1450, "suffix": "+", "order": 3})
        SiteMetric.objects.get_or_create(label="Laptops Restored", defaults={"value": 3200, "suffix": "+", "order": 4})

        # 10. Core Pillars
        CorePillar.objects.get_or_create(
            title="Web Solutions & Software",
            defaults={
                "description": "Custom web app development, Django backends, React interfaces, business websites, e-commerce platforms, and database architecture.",
                "icon_name": "globe",
                "button_text": "Explore Web Solutions",
                "button_link": "/services/?highlight=web",
                "features_list": "Fullstack Web Applications\nE-Commerce & Online Portals\nUI/UX Modernization & Redesigns",
                "order": 1
            }
        )
        CorePillar.objects.get_or_create(
            title="CCTV & Security Systems",
            defaults={
                "description": "HD & IP camera installation, NVR/DVR storage configuration, night vision infrared security, and live smartphone monitoring.",
                "icon_name": "video",
                "button_text": "View CCTV Kits",
                "button_link": "/cctv/",
                "features_list": "4K IP & ColorVu Night Vision\nRemote Mobile Live Streaming\nMotion Alerts & Cloud/NVR Storage",
                "order": 2
            }
        )
        CorePillar.objects.get_or_create(
            title="Network Gear & Cabling",
            defaults={
                "description": "Sales of enterprise routers, switches, fiber accessories, patch panels, Cat6 structured cabling, and high-speed Wi-Fi mesh.",
                "icon_name": "network",
                "button_text": "Networking Store",
                "button_link": "/networking/",
                "features_list": "Cisco, MikroTik & Ubiquiti Sales\nCat6/Cat6A Shielded Cabling\nEnterprise Server Rack Setup",
                "order": 3
            }
        )
        CorePillar.objects.get_or_create(
            title="Component-Level Laptop Repair",
            defaults={
                "description": "Screen replacements, motherboard micro-soldering, water damage restoration, thermal cleaning, and fast SSD storage upgrades.",
                "icon_name": "cpu",
                "button_text": "Get Repair Estimate",
                "button_link": "/repairs/",
                "features_list": "Screen & Keyboard Replacements\nWater Damage & Logic Board\nThermal Paste & SSD Upgrades",
                "order": 4
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded TechStyle Solutions database!"))
