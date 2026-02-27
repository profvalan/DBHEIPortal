from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsItem, NewsImage, SDGGoal, NewsCategory
from .forms import NewsItemForm, AdminReviewForm
from .serializers import NewsItemSerializer


# ── Public views ──────────────────────────────

def home(request):
    latest = NewsItem.objects.filter(status=NewsItem.STATUS_APPROVED).select_related(
        'institution', 'category'
    ).prefetch_related('sdg_goals')[:9]
    sdg_goals = SDGGoal.objects.all()
    categories = NewsCategory.objects.all()
    return render(request, 'news/home.html', {
        'latest_news': latest,
        'sdg_goals': sdg_goals,
        'categories': categories,
    })


def news_list(request):
    qs = NewsItem.objects.filter(status=NewsItem.STATUS_APPROVED).select_related(
        'institution', 'category'
    ).prefetch_related('sdg_goals')

    q = request.GET.get('q', '')
    sdg = request.GET.get('sdg', '')
    category = request.GET.get('category', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
    if sdg:
        qs = qs.filter(sdg_goals__number=sdg)
    if category:
        qs = qs.filter(category__slug=category)

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'news/list.html', {
        'page_obj': page,
        'sdg_goals': SDGGoal.objects.all(),
        'categories': NewsCategory.objects.all(),
        'q': q, 'sdg': sdg, 'category': category,
    })


def news_detail(request, slug):
    item = get_object_or_404(NewsItem, slug=slug, status=NewsItem.STATUS_APPROVED)
    related = NewsItem.objects.filter(
        status=NewsItem.STATUS_APPROVED,
        institution=item.institution
    ).exclude(pk=item.pk)[:4]
    return render(request, 'news/detail.html', {
        'item': item,
        'related': related,
        'embed_url': item.get_embed_url(),
    })


def sdg_news(request, number):
    sdg = get_object_or_404(SDGGoal, number=number)
    qs = NewsItem.objects.filter(
        status=NewsItem.STATUS_APPROVED, sdg_goals=sdg
    ).select_related('institution', 'category')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'news/sdg_news.html', {'sdg': sdg, 'page_obj': page})


# ── Institution dashboard views ───────────────

@login_required
def dashboard(request):
    if request.user.is_admin_user():
        return redirect('news:admin_dashboard')

    try:
        inst = request.user.institution
    except Exception:
        messages.error(request, 'No institution profile linked to your account.')
        return redirect('home')

    news_items = NewsItem.objects.filter(institution=inst).order_by('-created_at')
    stats = {
        'total': news_items.count(),
        'draft': news_items.filter(status=NewsItem.STATUS_DRAFT).count(),
        'pending': news_items.filter(status=NewsItem.STATUS_PENDING).count(),
        'approved': news_items.filter(status=NewsItem.STATUS_APPROVED).count(),
        'rejected': news_items.filter(status=NewsItem.STATUS_REJECTED).count(),
    }
    return render(request, 'news/dashboard.html', {
        'institution': inst,
        'news_items': news_items[:10],
        'stats': stats,
    })


@login_required
def news_create(request):
    if not request.user.is_institution_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')
    try:
        institution = request.user.institution
    except Exception:
        messages.error(request, 'No institution profile found.')
        return redirect('news:dashboard')

    if request.method == 'POST':
        form = NewsItemForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.institution = institution
            action = request.POST.get('action', 'draft')
            if action == 'submit':
                news.status = NewsItem.STATUS_PENDING
                news.submitted_at = timezone.now()
            else:
                news.status = NewsItem.STATUS_DRAFT
            news.save()
            form.save_m2m()

            for img in request.FILES.getlist('extra_images'):
                NewsImage.objects.create(news_item=news, image=img)

            if action == 'submit':
                messages.success(request, 'News submitted for admin approval.')
            else:
                messages.success(request, 'News saved as draft.')
            return redirect('news:my_news')
    else:
        form = NewsItemForm()

    return render(request, 'news/news_form.html', {
        'form': form,
        'sdg_goals': SDGGoal.objects.all(),
        'page_title': 'Post New Article',
    })


@login_required
def news_edit(request, pk):
    if not request.user.is_institution_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')
    try:
        institution = request.user.institution
    except Exception:
        messages.error(request, 'No institution profile found.')
        return redirect('news:dashboard')

    news = get_object_or_404(NewsItem, pk=pk, institution=institution)
    if news.status == NewsItem.STATUS_APPROVED:
        messages.warning(request, 'Approved articles cannot be edited.')
        return redirect('news:my_news')

    if request.method == 'POST':
        form = NewsItemForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news_item = form.save(commit=False)
            action = request.POST.get('action', 'draft')
            if action == 'submit':
                news_item.status = NewsItem.STATUS_PENDING
                news_item.submitted_at = timezone.now()
            else:
                news_item.status = NewsItem.STATUS_DRAFT
            news_item.save()
            form.save_m2m()

            for img in request.FILES.getlist('extra_images'):
                NewsImage.objects.create(news_item=news_item, image=img)

            messages.success(request, 'Article updated.')
            return redirect('news:my_news')
    else:
        form = NewsItemForm(instance=news)

    return render(request, 'news/news_form.html', {
        'form': form,
        'news': news,
        'sdg_goals': SDGGoal.objects.all(),
        'page_title': f'Edit: {news.title}',
    })


@login_required
def news_delete(request, pk):
    try:
        institution = request.user.institution
    except Exception:
        return redirect('news:dashboard')
    news = get_object_or_404(NewsItem, pk=pk, institution=institution)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Article deleted.')
    return redirect('news:my_news')


@login_required
def my_news(request):
    try:
        institution = request.user.institution
    except Exception:
        return redirect('news:dashboard')
    qs = NewsItem.objects.filter(institution=institution).prefetch_related('sdg_goals')
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'news/my_news.html', {
        'page_obj': page,
        'status_filter': status_filter,
    })


# ── Admin review views ────────────────────────

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')

    pending = NewsItem.objects.filter(status=NewsItem.STATUS_PENDING).select_related('institution')
    stats = {
        'pending': NewsItem.objects.filter(status=NewsItem.STATUS_PENDING).count(),
        'approved': NewsItem.objects.filter(status=NewsItem.STATUS_APPROVED).count(),
        'rejected': NewsItem.objects.filter(status=NewsItem.STATUS_REJECTED).count(),
        'total': NewsItem.objects.count(),
    }
    return render(request, 'news/admin_dashboard.html', {
        'pending_items': pending,
        'stats': stats,
    })


@login_required
def admin_review(request, pk):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('news:dashboard')

    news = get_object_or_404(NewsItem, pk=pk)

    if request.method == 'POST':
        form = AdminReviewForm(request.POST, instance=news)
        if form.is_valid():
            item = form.save(commit=False)
            if item.status == NewsItem.STATUS_APPROVED:
                item.published_at = timezone.now()
            item.save()
            messages.success(request, f'Decision saved: {item.get_status_display()}')
            return redirect('news:admin_dashboard')
    else:
        form = AdminReviewForm(instance=news)

    return render(request, 'news/admin_review.html', {
        'news': news,
        'form': form,
        'embed_url': news.get_embed_url(),
    })


@login_required
def admin_all_news(request):
    if not request.user.is_admin_user():
        return redirect('news:dashboard')
    qs = NewsItem.objects.all().select_related('institution', 'category')
    status_filter = request.GET.get('status', '')
    institution_filter = request.GET.get('institution', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if institution_filter:
        qs = qs.filter(institution__id=institution_filter)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))

    from institutions.models import Institution
    return render(request, 'news/admin_all_news.html', {
        'page_obj': page,
        'status_filter': status_filter,
        'institutions': Institution.objects.all(),
    })


# ── REST API ──────────────────────────────────

@api_view(['GET'])
def api_news_list(request):
    qs = NewsItem.objects.filter(status=NewsItem.STATUS_APPROVED).select_related(
        'institution', 'category'
    ).prefetch_related('sdg_goals')

    sdg = request.query_params.get('sdg')
    institution = request.query_params.get('institution')
    q = request.query_params.get('q')

    if sdg:
        qs = qs.filter(sdg_goals__number=sdg)
    if institution:
        qs = qs.filter(institution__id=institution)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q))

    serializer = NewsItemSerializer(qs[:50], many=True, context={'request': request})
    return Response({'count': qs.count(), 'results': serializer.data})


@api_view(['GET'])
def api_news_detail(request, slug):
    item = get_object_or_404(NewsItem, slug=slug, status=NewsItem.STATUS_APPROVED)
    serializer = NewsItemSerializer(item, context={'request': request})
    return Response(serializer.data)
