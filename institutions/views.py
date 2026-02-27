from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from .models import Institution, InstitutionStats
from .forms import InstitutionProfileForm, InstitutionStatsForm


# ── Public views ──────────────────────────────

def institution_directory(request):
    """Public page listing all institutions with key stats."""
    qs = Institution.objects.filter(is_active=True).select_related('stats')

    province = request.GET.get('province', '')
    category = request.GET.get('category', '')
    inst_type = request.GET.get('type', '')
    q = request.GET.get('q', '')

    if province:
        qs = qs.filter(province=province)
    if category:
        qs = qs.filter(institution_category=category)
    if inst_type:
        qs = qs.filter(institution_type=inst_type)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(place__icontains=q))

    from .models import PROVINCE_CHOICES, INSTITUTION_CATEGORY_CHOICES, INSTITUTION_TYPE_CHOICES
    all_institutions = Institution.objects.filter(is_active=True)
    aggregate = InstitutionStats.objects.filter(institution__is_active=True).aggregate(
        total_students=Sum('total_students'),
        total_faculty=Sum('total_faculty'),
        total_programs=Sum('total_programs'),
        total_research=Sum('research_papers'),
    )

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'institutions/directory.html', {
        'page_obj': page,
        'aggregate': aggregate,
        'total_institutions': all_institutions.count(),
        'province_choices': PROVINCE_CHOICES,
        'category_choices': INSTITUTION_CATEGORY_CHOICES,
        'type_choices': INSTITUTION_TYPE_CHOICES,
        'province': province,
        'category': category,
        'inst_type': inst_type,
        'q': q,
    })


def institution_detail(request, pk):
    """Public detail page for a single institution with stats."""
    inst = get_object_or_404(Institution, pk=pk, is_active=True)
    stats = getattr(inst, 'stats', None)

    from news.models import NewsItem
    recent_news = NewsItem.objects.filter(
        institution=inst, status=NewsItem.STATUS_APPROVED
    ).order_by('-published_at')[:5]

    return render(request, 'institutions/detail.html', {
        'institution': inst,
        'stats': stats,
        'recent_news': recent_news,
    })


# ── Institution self-edit views ───────────────

@login_required
def edit_profile(request):
    """Institution edits their own profile."""
    if not request.user.is_institution_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')
    try:
        inst = request.user.institution
    except Exception:
        messages.error(request, 'No institution profile found.')
        return redirect('news:dashboard')

    if request.method == 'POST':
        form = InstitutionProfileForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('institutions:edit_profile')
    else:
        form = InstitutionProfileForm(instance=inst)

    return render(request, 'institutions/edit_profile.html', {
        'form': form,
        'institution': inst,
    })


@login_required
def edit_stats(request):
    """Institution edits their own statistics."""
    if not request.user.is_institution_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')
    try:
        inst = request.user.institution
    except Exception:
        messages.error(request, 'No institution profile found.')
        return redirect('news:dashboard')

    stats, _ = InstitutionStats.objects.get_or_create(institution=inst)

    if request.method == 'POST':
        form = InstitutionStatsForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statistics updated successfully.')
            return redirect('institutions:edit_stats')
    else:
        form = InstitutionStatsForm(instance=stats)

    return render(request, 'institutions/edit_stats.html', {
        'form': form,
        'institution': inst,
        'stats': stats,
    })


# ── Admin views ───────────────────────────────

@login_required
def admin_institution_list(request):
    """Admin overview of all institutions and their stats."""
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')

    qs = Institution.objects.all().select_related('stats')
    province = request.GET.get('province', '')
    if province:
        qs = qs.filter(province=province)

    from .models import PROVINCE_CHOICES
    aggregate = InstitutionStats.objects.aggregate(
        total_students=Sum('total_students'),
        total_faculty=Sum('total_faculty'),
        total_programs=Sum('total_programs'),
        total_research=Sum('research_papers'),
    )

    return render(request, 'institutions/admin_list.html', {
        'institutions': qs,
        'province_choices': PROVINCE_CHOICES,
        'province': province,
        'aggregate': aggregate,
        'total_count': qs.count(),
    })


@login_required
def admin_edit_institution(request, pk):
    """Admin can edit any institution's profile and stats."""
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')

    inst = get_object_or_404(Institution, pk=pk)
    stats, _ = InstitutionStats.objects.get_or_create(institution=inst)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'profile':
            form = InstitutionProfileForm(request.POST, request.FILES, instance=inst)
            stats_form = InstitutionStatsForm(instance=stats)
            if form.is_valid():
                form.save()
                messages.success(request, f'Profile updated for {inst.name}.')
                return redirect('institutions:admin_edit', pk=pk)
        else:
            form = InstitutionProfileForm(instance=inst)
            stats_form = InstitutionStatsForm(request.POST, instance=stats)
            if stats_form.is_valid():
                stats_form.save()
                messages.success(request, f'Statistics updated for {inst.name}.')
                return redirect('institutions:admin_edit', pk=pk)
    else:
        form = InstitutionProfileForm(instance=inst)
        stats_form = InstitutionStatsForm(instance=stats)

    return render(request, 'institutions/admin_edit.html', {
        'institution': inst,
        'form': form,
        'stats_form': stats_form,
        'stats': stats,
    })
