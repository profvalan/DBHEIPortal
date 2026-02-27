"""
Management command to seed the database with:
- Admin user
- All 17 SDG goals
- Default news categories
- 48 Don Bosco Higher Education Institutions with logins
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from news.models import SDGGoal, NewsCategory
from institutions.models import Institution, InstitutionStats

User = get_user_model()

# (No, Province, Name, Place, Website, Foundation Year, Category key, Type key)
INSTITUTIONS = [
    (1,  'Bengaluru', 'Don Bosco Arts and Science College Angikadavu', 'Angikadavu', 'https://www.donbosco.ac.in/', 2003, 'affiliated', 'college'),
    (2,  'Bengaluru', 'Don Bosco College Mannuthy', 'Mannuthy', 'https://dbcollegemannuthy.edu.in/home', 2005, 'affiliated', 'college'),
    (3,  'Bengaluru', 'Don Bosco College Wayanad', 'Wayanad', 'https://dbcollegebathery.ac.in/', 2005, 'affiliated', 'college'),
    (4,  'Bengaluru', 'Don Bosco Institutions Yadgiri', 'Yadgiri', 'http://www.donboscoyadgiri.org/', 2012, 'affiliated', 'college'),
    (5,  'Bengaluru', 'Don Bosco Arts and Science College Mampetta', 'Mampetta', 'https://www.dbcmampetta.ac.in/', 2013, 'affiliated', 'college'),
    (6,  'Bengaluru', 'Don Bosco College Kottiam', 'Kottiam', 'https://donbosco.college/', 2015, 'affiliated', 'college'),
    (7,  'Bengaluru', 'Don Bosco Degree College Chitradurga', 'Chitradurga', 'https://donboscodegreecollegechitradurga.com/', 2020, 'affiliated', 'college'),
    (8,  'Bengaluru', 'Don Bosco College Bengaluru', 'Bengaluru', 'https://dbcblr.edu.in/', 2021, 'affiliated', 'college'),
    (9,  'Chennai', 'Sacred Heart College (Autonomous) Tirupattur', 'Tirupattur', 'https://shctpt.edu/', 1951, 'autonomous', 'college'),
    (10, 'Chennai', 'SIGA Polytechnic College Chennai-Rinaldi', 'Chennai', 'https://www.donboscochennai.org/rinaldi-juniorate-siga', 1952, 'technical', 'college'),
    (11, 'Chennai', 'Don Bosco College Dharmapuri', 'Dharmapuri', 'https://dbcdharmapuri.edu.in/', 2007, 'affiliated', 'college'),
    (12, 'Chennai', 'Don Bosco Polytechnic College Thirukazhukundram', 'Thirukazhukundram', 'https://dbpolytechnictkm.com/', 2009, 'technical', 'college'),
    (13, 'Chennai', 'Don Bosco College of Education Dharmapuri', 'Dharmapuri', 'https://www.dbcedharmapuri.com/', 2012, 'affiliated', 'college'),
    (14, 'Chennai', 'Don Bosco College (Arts and Science) Karaikal', 'Karaikal', 'http://dbckaraikal.in/', 2012, 'affiliated', 'college'),
    (15, 'Chennai', 'Don Bosco College (Co-Ed) Yelagiri Hills', 'Yelagiri Hills', 'https://www.dbcyelagiri.edu.in/', 2012, 'affiliated', 'college'),
    (16, 'Chennai', 'Don Bosco Polytechnic College Chennai-Basin Bridge', 'Chennai', 'https://www.dbtechcampus.ac.in/', 2014, 'technical', 'college'),
    (17, 'Chennai', 'Don Bosco College Agriculture Sagayathottam', 'Sagayathottam', 'https://www.dbca.ac.in/', 2014, 'technical', 'college'),
    (18, 'Chennai', 'Don Bosco College of Arts and Science Chennai', 'Chennai', 'https://dbcc.edu.in/', 2016, 'affiliated', 'college'),
    (19, 'Dimapur', 'Salesian College of Higher Education Dimapur', 'Dimapur', 'http://schedimapur.edu.in/', 1995, 'affiliated', 'college'),
    (20, 'Dimapur', 'Don Bosco College Maram', 'Maram', 'https://dbcmaram.ac.in/', 2000, 'autonomous', 'college'),
    (21, 'Dimapur', 'Don Bosco College Itanagar', 'Itanagar', 'https://dbcitanagar.ac.in/', 2002, 'affiliated', 'college'),
    (22, 'Dimapur', 'Don Bosco College of Teacher Education Dimapur', 'Dimapur', 'https://boscocollegedimapur.in/', 2003, 'affiliated', 'college'),
    (23, 'Dimapur', 'Bosco Institute Jorhat', 'Jorhat', 'https://boscoinstitute.org/', 2008, 'affiliated', 'college'),
    (24, 'Dimapur', 'Don Bosco College Golaghat', 'Golaghat', 'https://dbcgolaghat.edu.in/', 2016, 'affiliated', 'college'),
    (25, 'Dimapur', 'Don Bosco College Kohima', 'Kohima', 'https://www.dbckohima.ac.in/', 2005, 'affiliated', 'college'),
    (26, 'Guwahati', 'Don Bosco College Tura', 'Tura', 'https://www.donboscocollege.ac.in/', 1987, 'affiliated', 'college'),
    (27, 'Guwahati', 'Don Bosco College of Teacher Education Tura', 'Tura', 'http://dbctetura.in/', 2003, 'affiliated', 'college'),
    (28, 'Guwahati', 'Assam Don Bosco University Guwahati', 'Guwahati', 'https://www.dbuniversity.ac.in/index.php', 2008, 'university', 'university'),
    (29, 'Guwahati', 'Don Bosco College Chapaguri', 'Chapaguri', 'http://donboscocollege.org.in/', 2019, 'affiliated', 'college'),
    (30, 'Guwahati', 'Don Bosco College Diphu', 'Diphu', 'http://www.dbcdiphu.edu.in/', 2018, 'affiliated', 'college'),
    (31, 'Guwahati', 'Don Bosco Institute of Management Guwahati', 'Guwahati', 'https://dbim.ac.in/', 2015, 'affiliated', 'college'),
    (32, 'Hyderabad', 'Bosco Degree College Hyderabad', 'Hyderabad', 'https://dbdchyd.ac.in/', 2000, 'affiliated', 'college'),
    (33, 'Hyderabad', 'Don Bosco College Narsipatnam', 'Narsipatnam', 'https://donboscocollegenarsipatnam.com/', 2007, 'affiliated', 'college'),
    (34, 'Hyderabad', 'Don Bosco Academy Nalgonda', 'Nalgonda', 'https://www.donboscoacademynalgonda.com/', 2008, 'affiliated', 'college'),
    (35, 'Kolkatta', 'Salesian College of Higher Education Sonada/Siliguri', 'Sonada/Siliguri', 'https://salesiancollege.ac.in/', 1933, 'autonomous', 'college'),
    (36, 'Mumbai', 'Don Bosco Institute of Technology Kurla', 'Kurla', 'https://www.dbit.in/', 2001, 'technical', 'college'),
    (37, 'Mumbai', 'Don Bosco College Kurla', 'Kurla', 'https://www.donboscocollege.in/', 2011, 'affiliated', 'college'),
    (38, 'Mumbai', 'Don Bosco College of Commerce Yerwada', 'Yerwada', 'https://www.donboscocollegepune.com/', 2013, 'affiliated', 'college'),
    (39, 'New Delhi', 'Don Bosco Institute of Technology (DBIT) Okhla', 'Okhla', 'https://www.donboscoitggsipu.org/', 2022, 'affiliated', 'college'),
    (40, 'New Delhi', 'Don Bosco Degree College (DBDC) Jhansi', 'Jhansi', 'https://dbdcjhansi.com/', 2022, 'affiliated', 'college'),
    (41, 'Panjim', 'Don Bosco College Panjim', 'Panjim', 'https://donboscogoa.ac.in/', 2001, 'affiliated', 'college'),
    (42, 'Panjim', 'Don Bosco College of Engineering Fatorda', 'Fatorda', 'https://dbcegoa.ac.in/', 2011, 'technical', 'college'),
    (43, 'Shillong', "St. Antony's College Shillong", 'Shillong', 'https://anthonys.ac.in/', 1934, 'affiliated', 'college'),
    (44, 'Shillong', 'Don Bosco College Byndihati', 'Byndihati', 'https://www.donboscocollegebyndi.ac.in/', 2014, 'affiliated', 'college'),
    (45, 'Tiruchy', 'Pastor Lenssen Polytechnic College Kuthenkuly', 'Kuthenkuly', 'https://donboscoplpc.com/', 2001, 'technical', 'college'),
    (46, 'Tiruchy', 'Don Bosco Polytechnic College Tharangambadi', 'Tharangambadi', 'https://donboscopolytharangam.org/', 2008, 'technical', 'college'),
    (47, 'Tiruchy', 'Don Bosco Arts and Science College Keela Eral', 'Keela Eral', 'https://www.dbcas.edu.in/home/', 2014, 'affiliated', 'college'),
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


def make_username(num, name):
    """Generate a clean username like inst01, inst02, etc."""
    return f"inst{num:02d}"


class Command(BaseCommand):
    help = 'Seed database with admin, 17 SDG goals, categories, and 48 institutions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Delete all existing institutions and users (except admin) before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        if options.get('reset'):
            self.stdout.write('  Resetting existing institution data...')
            Institution.objects.all().delete()
            User.objects.filter(role='institution').delete()
            self.stdout.write(self.style.WARNING('  Cleared all institution data.\n'))

        # 1. Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@prems.edu.in',
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
            NewsCategory.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})
        self.stdout.write(self.style.SUCCESS(f'  Created {len(CATEGORIES)} news categories'))

        # 4. Institutions
        created = 0
        for num, prov, name, place, website, year, category, inst_type in INSTITUTIONS:
            username = make_username(num, name)
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@prems.edu.in',
                    password='Inst@1234',
                    role='institution',
                    first_name=name[:30],
                    last_name='HEI',
                )
                inst = Institution.objects.create(
                    user=user,
                    name=name,
                    short_name=f'HEI-{num:02d}',
                    website=website,
                    place=place,
                    province=prov,
                    foundation_year=year,
                    institution_category=category,
                    institution_type=inst_type,
                    contact_email=f'{username}@prems.edu.in',
                )
                # Create empty stats row for each institution
                InstitutionStats.objects.get_or_create(institution=inst)
                created += 1

        self.stdout.write(self.style.SUCCESS(f'  Created {created} institution accounts'))
        self.stdout.write(self.style.SUCCESS(f'\nDone! Seed data loaded successfully.'))

        self.stdout.write('\n' + '='*55)
        self.stdout.write('  LOGIN CREDENTIALS')
        self.stdout.write('='*55)
        self.stdout.write(f'  Admin:    admin / Admin@1234')
        self.stdout.write(f'  Default password for all institutions: Inst@1234')
        self.stdout.write('')
        self.stdout.write(f'  {"No":<4} {"Username":<10} {"Institution Name"}')
        self.stdout.write(f'  {"-"*4} {"-"*10} {"-"*45}')
        for num, prov, name, place, website, year, cat, itype in INSTITUTIONS:
            self.stdout.write(f'  {num:<4} {make_username(num, name):<10} {name[:45]}')
        self.stdout.write('='*55)
