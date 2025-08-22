from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import GeneralInfo, Service, Testimonial, ContactFormLog, Blog

def index(request):
    general_info = GeneralInfo.objects.first()
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()

    for testimonial in testimonials:
        testimonial.stars = ['x'] * testimonial.rating_count

    recent_blogs = Blog.objects.all().order_by("-created_at")[:3]
     
    default_value = ""
    context = {
        "company_name": getattr(general_info, "company_name", default_value),
        "location": getattr(general_info, "location", default_value),
        "email": getattr(general_info, "email", default_value),
        "phone": getattr(general_info, "phone", default_value),
        "open_hours": getattr(general_info, "open_hours", default_value),
        "video_url": getattr(general_info, "video_url", default_value),
        "twitter_url": getattr(general_info, "twitter-url", default_value),
        "facebook_url": getattr(general_info, "facebook_url", default_value),
        "instagram_url": getattr(general_info, "instagram_url", default_value),
        "linkedin_url": getattr(general_info, "linkedin_url", default_value),
        "services": services,
        "testimonials": testimonials,
        "recent_blogs": recent_blogs,
    }
    
    return render(request, "index.html", context)

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        context = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "action_time": timezone.now()
        }
        html_content = render_to_string('email.html', context)

        is_success = False
        is_error = False
        error_message = ""

        try:
            # Send email to admin
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"""
                New message from your website contact form:
                
                Name: {name}
                Email: {email}
                Subject: {subject}
                Message: {message}
                
                Time: {timezone.now()}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
                html_message=html_content,
            )
            
            # Send confirmation email to the person who submitted the form
            send_mail(
                subject="Thank you for contacting us",
                message=f"""
                Dear {name},

                Thank you for contacting us. We have received your message and will get back to you soon.

                Your message details:
                Subject: {subject}
                Message: {message}

                Best regards,
                Your Company Name
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            is_success = True
            messages.success(request, "Your message has been sent successfully!")
            
        except Exception as e:
            is_error = True
            error_message = str(e)
            messages.error(request, f"Error sending email: {error_message}")
            
        # Log the contact form submission
        ContactFormLog.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            action_time=timezone.now(),
            is_success=is_success,
            is_error=is_error,
            error_message=error_message,
        )

    return redirect('home')

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    recent_blogs = Blog.objects.all().exclude(id=blog_id).order_by("-created_at")[:2]

    context = {
        "blog": blog,
        "recent_blogs": recent_blogs,
    }
    return render(request, "blog_details.html", context)

def blogs(request):
    all_blogs = Blog.objects.all().order_by("-created_at")
    blogs_per_page = 3
    paginator = Paginator(all_blogs, blogs_per_page)
    page = request.GET.get('page', 1)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        "blogs": blogs,
    }
    return render(request, "blogs.html", context)
