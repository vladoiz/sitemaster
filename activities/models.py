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
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase, Tag as TaggitTag
from taggit.managers import TaggableManager
from wagtail.documents.edit_handlers import DocumentChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


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

class AchievementCategory(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['AchievementPage']

    def get_context(self, request):
        context = super().get_context(request)
        achievements = AchievementPage.objects.child_of(self).live().order_by('-date')

        # Pagination for achievements
        paginator = Paginator(achievements, 10)  # Show 10 achievements per page
        page = request.GET.get('page')
        try:
            achievements = paginator.page(page)
        except PageNotAnInteger:
            achievements = paginator.page(1)
        except EmptyPage:
            achievements = paginator.page(paginator.num_pages)

        context['achievements'] = achievements
        return context

class AchievementPage(Page):
    description = RichTextField(blank=True)
    date = models.DateField(default=timezone.now)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('date'),
        ImageChooserPanel('image'),
        DocumentChooserPanel('document'),
    ]

    def __str__(self):
        return self.title

class AchievementIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['AchievementCategory']

    def get_context(self, request):
        context = super().get_context(request)
        categories = AchievementCategory.objects.child_of(self).live().order_by('-first_published_at')

        # Pagination for categories
        paginator = Paginator(categories, 10)  # Show 10 categories per page
        page = request.GET.get('page')
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)

        context['categories'] = categories
        return context