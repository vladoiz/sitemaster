from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class CourseGalleryImage(models.Model):
    page = ParentalKey('CoursePage', related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return self.caption or "Image"


class CoursePage(Page):
    course_name = models.CharField(max_length=255, blank=True)
    full_cost = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    group_cost = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_hours = models.PositiveIntegerField(help_text="Общий объем занятий в часах", blank=True, null=True)
    description = models.TextField(help_text="Краткая запись о том, что будет освоено на курсе", blank=True)
    skills = models.TextField(help_text="Некоторые конкретные навыки", blank=True)
    program_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    contact_info = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('course_name'),
        FieldPanel('full_cost'),
        FieldPanel('group_cost'),
        FieldPanel('total_hours'),
        FieldPanel('description'),
        FieldPanel('skills'),
        DocumentChooserPanel('program_document'),
        FieldPanel('contact_info'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('course_name'),
        index.SearchField('description'),
        index.SearchField('skills'),
    ]

    template = "courses/course_page.html"


class ClubPage(Page):
    club_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(help_text="Краткая запись о том, что будет освоено в кружке", blank=True)
    contact_info = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('club_name'),
        FieldPanel('description'),
        FieldPanel('contact_info'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('club_name'),
        index.SearchField('description'),
    ]

    template = "courses/club_page.html"


class CourseIndexPage(Page):
    subpage_types = ['CoursePage', 'ClubPage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        courses = CoursePage.objects.child_of(self).live().order_by('-first_published_at')
        clubs = ClubPage.objects.child_of(self).live().order_by('-first_published_at')
        context['courses'] = courses
        context['clubs'] = clubs
        return context

    content_panels = Page.content_panels + [
        FieldPanel('title', classname="full"),
    ]

    template = "courses/course_index_page.html"
