"""
Management command to seed the database with:
- Admin user
- All 17 SDG goals
- Default news categories
- 51 Higher Education Institutions with logins
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import SDGGoal, NewsCategory
from institutions.models import Institution

User = get_user_model()

INSTITUTIONS = [
    ("University of Colombo", "UOC"),
    ("University of Peradeniya", "UOP"),
    ("University of Sri Jayewardenepura", "USJ"),
    ("University of Kelaniya", "UOK"),
    ("University of Moratuwa", "UOM"),
    ("University of Jaffna", "UOJ"),
    ("University of Ruhuna", "UOR"),
    ("Eastern University Sri Lanka", "EUSL"),
    ("South Eastern University of Sri Lanka", "SEUSL"),
    ("Rajarata University of Sri Lanka", "RUSL"),
    ("Sabaragamuwa University of Sri Lanka", "SUSL"),
    ("Wayamba University of Sri Lanka", "WUSL"),
    ("Uva Wellassa University", "UWU"),
    ("University of the Visual and Performing Arts", "UVPA"),
    ("Open University of Sri Lanka", "OUSL"),
    ("Sri Lanka Institute of Information Technology", "SLIIT"),
    ("Kotelawala Defence University", "KDU"),
    ("Sri Lanka Technological Campus", "SLTC"),
    ("NSBM Green University", "NSBM"),
    ("Horizon Campus", "HC"),
    ("Informatics Institute of Technology", "IIT"),
    ("ICBT Campus", "ICBT"),
    ("Asia Pacific Institute of Information Technology", "APIIT"),
    ("Sri Lanka Institute of Advanced Technological Education", "SLIATE"),
    ("National Institute of Education", "NIE"),
    ("Postgraduate Institute of Science", "PGIS"),
    ("Postgraduate Institute of Medicine", "PGIM"),
    ("Postgraduate Institute of Agriculture", "PGIA"),
    ("Postgraduate Institute of Archaeology", "PGIAR"),
    ("Sri Lanka Institute of Nanotechnology", "SLINTEC"),
    ("National School of Business Management", "NSBM-B"),
    ("Sri Lanka Institute of Marketing", "SLIM"),
    ("Chartered Institute of Management Accountants Sri Lanka", "CIMA-SL"),
    ("Institute of Chartered Accountants of Sri Lanka", "CA-SL"),
    ("Sri Lanka Law College", "SLLC"),
    ("Bandaranaike Centre for International Studies", "BCIS"),
    ("Sri Lanka Foundation Institute", "SLFI"),
    ("Arthur C Clarke Institute", "ACCI"),
    ("Industrial Technology Institute", "ITI"),
    ("Sri Lanka Standards Institution", "SLSI"),
    ("National Institute of Fisheries and Nautical Engineering", "NIFNE"),
    ("Sri Lanka Vocational Training Authority", "VTA"),
    ("National Youth Services Council", "NYSC"),
    ("Sri Lanka School of Tourism and Hospitality Management", "SLSTHM"),
    ("Chartered Institute of Personnel Management Sri Lanka", "CIPM"),
    ("Institute of Engineers Sri Lanka", "IESL"),
    ("Sri Lanka Medical Association", "SLMA"),
    ("Postgraduate Institute of Management", "PIM"),
    ("University of Colombo School of Computing", "UCSC"),
    ("Buddhist and Pali University of Sri Lanka", "BPU"),
    ("Sri Lanka International Buddhist Academy", "SIBA"),
]

CATEGORIES = [
    "Research & Innovation",
    "Student Affairs",
    "Industry Partnerships",
    "Community Engagement",
    "International Relations",
    "Awards & Recognition",
    "Events & Conferences",
    "Sustainability",
    "Technology & Digital",
    "Health & Wellbeing",
]


class Command(BaseCommand):
    help = 'Seed database with admin, 17 SDG goals, categories, and 51 institutions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # 1. Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@prems.lk',
                password='Admin@1234',
                role='admin',
                first_name='Portal',
                last_name='Admin',
            )
            self.stdout.write(self.style.SUCCESS('  Created admin user (admin / Admin@1234)'))
        else:
            self.stdout.write('  Admin user already exists')

        # 2. SDG Goals
        for number, _ in SDGGoal._meta.get_field('number').choices:
            SDGGoal.objects.get_or_create(number=number)
        self.stdout.write(self.style.SUCCESS('  Created 17 SDG goals'))

        # 3. News Categories
        for cat_name in CATEGORIES:
            from django.utils.text import slugify
            NewsCategory.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})
        self.stdout.write(self.style.SUCCESS(f'  Created {len(CATEGORIES)} news categories'))

        # 4. Institutions
        created = 0
        for name, short_name in INSTITUTIONS:
            username = short_name.lower().replace('-', '_').replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@prems.lk',
                    password='Inst@1234',
                    role='institution',
                    first_name=short_name,
                    last_name='Portal',
                )
                Institution.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': name,
                        'short_name': short_name,
                        'contact_email': f'news@{username.replace("_","")}.lk',
                    }
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f'  Created {created} institution accounts'))
        self.stdout.write(self.style.SUCCESS('\nDone! Seed data loaded successfully.'))
        self.stdout.write('\nCredentials:')
        self.stdout.write('  Admin:       admin / Admin@1234')
        self.stdout.write('  Institutions: <short_name_lowercase> / Inst@1234')
        self.stdout.write('  Example:     uoc / Inst@1234')
