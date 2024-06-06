from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

class ActivityBlogPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField("Post date", default=timezone.now)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),
        FieldPanel('body')
    ]

class ActivityStructurePage(Page):
    intro = models.TextField(blank=True)
    documentation = StreamField([
        ('document', DocumentChooserBlock())
    ], use_json_field=True, blank=True, null=True, verbose_name='Документация')

    body = StreamField([
        ('carousel', blocks.StreamBlock([
            ('image', ImageChooserBlock()),
            ('video', EmbedBlock()),
        ]))
    ], use_json_field=True, blank=True, null=True, verbose_name='Фотографии слайдера')

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        StreamFieldPanel('documentation'),
    ]

    def get_blog_posts(self):
        return ActivityBlogPage.objects.live().descendant_of(self).order_by('-first_published_at')

    def get_context(self, request):
        context = super().get_context(request)
        blog_posts = self.get_blog_posts()

        # Pagination for blog posts
        paginator = Paginator(blog_posts, 5)  # Show 5 blog posts per page
        page = request.GET.get('page')
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        context['blog_posts'] = blog_posts
        return context

class ActivityIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        structures = ActivityStructurePage.objects.child_of(self).live().order_by('-first_published_at')
        
        # Pagination for structures
        paginator = Paginator(structures, 10)  # Show 10 structures per page
        page = request.GET.get('page')
        try:
            structures = paginator.page(page)
        except PageNotAnInteger:
            structures = paginator.page(1)
        except EmptyPage:
            structures = paginator.page(paginator.num_pages)

        context['structures'] = structures
        return context
