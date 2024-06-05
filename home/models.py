from django.shortcuts import render

from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RawHTMLBlock
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.search.models import Query
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.search import index


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


class Student(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class Sveden(Page):
    body = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
class StudentInclude(Page):
	body = StreamField([
	('HTML', RawHTMLBlock())
	], blank=True)
	content_panels = Page.content_panels + [
	StreamFieldPanel('body')
     ]
class Abiturient(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


    

class ActivityTile(models.Model):
    id = models.BigAutoField(primary_key=True)
    page = ParentalKey(
        'ActivityIndexPage', 
        related_name='tiles', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, help_text="Bootstrap иконка, например 'bi bi-cpu-fill")
    background_color = models.CharField(max_length=7, help_text="Цвет фона в формате hex, например '#ecebff'")
    icon_color = models.CharField(max_length=7, help_text="Цвет иконки в формате hex, например '#8660fe'")
    link = models.URLField(help_text="Ссылка на деятельность")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('background_color'),
        FieldPanel('icon_color'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.title

class ActivityIndexPage(Page):
    subpage_types = []  # No subpages allowed
    
    content_panels = Page.content_panels + [
        InlinePanel('tiles', label="Деятельность техникума")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['tiles'] = self.tiles.all()
        return context
    
class ActivityPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
    ])
    
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]


#функция поиска

def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
