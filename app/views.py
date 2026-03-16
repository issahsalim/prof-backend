from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail

from .models import (
    Profile, Research, Publication, Project, Award, CVFile,
    ContactMessage, GalleryImage,
)

def index(request):
   return render(request,'index.html')


def _build_absolute_uri(request, path):
    if not path:
        return None
    return request.build_absolute_uri(path) if request else str(path)


@require_GET
def api_profile(request):
    """Get profile (hero image and about text only). Single row."""
    obj = Profile.objects.first()
    if not obj:
        return JsonResponse({'about_text': '', 'hero_image': None})
    return JsonResponse({
        'about_text': obj.about_text,
        'hero_image': _build_absolute_uri(request, obj.hero_image.url) if obj.hero_image else None,
    })


@require_GET
def api_research(request):
    page = request.GET.get('page', 1)
    per_page = min(int(request.GET.get('per_page', 10)), 50)
    qs = Research.objects.all()
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    items = [
        {
            'id': r.id, 
            'title': r.title,
            'description': r.description,
            'link_url': r.link_url,
            'link_text': r.link_text or 'Read more',
        } 
        for r in page_obj.object_list
    ]
    return JsonResponse({
        'results': items,
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@require_GET
def api_publications(request):
    page = request.GET.get('page', 1)
    per_page = min(int(request.GET.get('per_page', 10)), 50)
    qs = Publication.objects.all()
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    items = [
        {
            'id': pbl.id,
            'title': pbl.title,
            'description': pbl.description,
            'link_url': pbl.link_url,
            'link_text': pbl.link_text or 'Read more',
        }
        for pbl in page_obj.object_list
    ]
    return JsonResponse({
        'results': items,
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@require_GET
def api_projects(request):
    page = request.GET.get('page', 1)
    per_page = min(int(request.GET.get('per_page', 10)), 50)
    qs = Project.objects.all()
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    items = [
        {
            'id': prj.id,
            'title': prj.title,
            'description': prj.description,
            'link_url': prj.link_url,
            'link_text': prj.link_text or 'Read more',
        }
        for prj in page_obj.object_list
    ]
    return JsonResponse({
        'results': items,
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@require_GET
def api_awards(request):
    page = request.GET.get('page', 1)
    per_page = min(int(request.GET.get('per_page', 10)), 50)
    qs = Award.objects.all()
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    items = [
        { 
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'image': _build_absolute_uri(request, a.image.url) if a.image else None,
        }
        for a in page_obj.object_list
    ]
    return JsonResponse({
        'results': items,
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@require_GET
def api_cv(request):
    """Get active CV download URL."""
    obj = CVFile.objects.filter(is_active=True).order_by('-uploaded_at').first()
    if not obj or not obj.file:
        return JsonResponse({'url': None, 'label': None})
    return JsonResponse({
        'url': _build_absolute_uri(request, obj.file.url),
        'label': obj.label or 'Download CV',
    })


@require_GET
def api_gallery(request):
    page = request.GET.get('page', 1)
    per_page = min(int(request.GET.get('per_page', 12)), 50)
    qs = GalleryImage.objects.all()
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    items = [
        {
            'id': g.id,
            'title': g.title,
            'image': _build_absolute_uri(request, g.image.url) if g.image else None,
        }
        for g in page_obj.object_list
    ]
    return JsonResponse({
        'results': items,
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@require_GET
def api_stats(request):
    """Counts for research, publications, projects, awards, gallery (for stats section)."""
    return JsonResponse({
        'research_count': Research.objects.count(),
        'publications_count': Publication.objects.count(),
        'projects_count': Project.objects.count(),
        'awards_count': Award.objects.count(),
        'gallery_count': GalleryImage.objects.count(),
    })


@csrf_exempt
@require_http_methods(['POST'])
def api_contact(request):
    """Accept contact form: save message, send email to user (confirmation) and to site owner."""
    import json
    print('[Contact] Request received')  # Debug: confirm view is hit
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        print('[Contact] Invalid JSON')
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    subject = (data.get('subject') or '').strip()
    message = (data.get('message') or '').strip()
    if not name or not email or not message:
        print('[Contact] Validation failed: name, email and message required')
        return JsonResponse({'success': False, 'error': 'Name, email and message are required'}, status=400)
    # Save to DB 
    ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
    print(f'[Contact] Saved message from {name} <{email}>')
    to_email = getattr(settings, 'CONTACT_EMAIL_TO', None) or settings.DEFAULT_FROM_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL
    # Email 1: confirmation to user (prints to console when EMAIL_BACKEND is console)
    try: 
        send_mail(
            subject='I received your message – Dr. Haruna Gado Yakubu',
            message=f'Dear {name},\n\nThank you for reaching out. I have received your message and will get back to you soon.\n\nBest regards,\nDr. Haruna Gado Yakubu',
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
        )
        print('[Contact] Confirmation email "sent" (see console output above)')
    except Exception as e:
        print(f'[Contact] Confirmation email failed: {e}')
    # Email 2: notification to site owner
    try:
        send_mail(
            subject=f'Portfolio contact: {subject or "New message"}',
            message=f'From: {name} <{email}>\nSubject: {subject or "(no subject)"}\n\n{message}',
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False,
        )
        print('[Contact] Owner notification "sent" (see console output above)')
    except Exception as e:
        print(f'[Contact] Owner notification failed: {e}')
    return JsonResponse({'success': True})
