from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField,StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import RawHTMLBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class SpecialtyPage(Page):
    body = StreamField([
    ('carousel', blocks.StreamBlock([
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
    ]) )
    ], use_json_field=True, blank=True,null=True, verbose_name='Фотографии слайдера')
    related_document = models.ForeignKey(
        'wagtaildocs.Document',verbose_name='Учебная программа', blank=True, null=True,
         on_delete=models.SET_NULL, related_name='+'
    )
    time = models.CharField(max_length=250, blank=True,verbose_name='Сроки обучения')
    p = RichTextField(blank=True, verbose_name='Текст описания')
    html = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True, verbose_name='Видео', null=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        DocumentChooserPanel('related_document'),
        FieldPanel('time'),
        FieldPanel('p'),
        StreamFieldPanel('html')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('p'),
        ]


class SpecialtyIndexPage(Page):
    intro = RichTextField(blank=True)
    html = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True,null=True )

    content_panels = Page.content_panels + [
        StreamFieldPanel('html')
    ]
    @property
    def specialty(self):
        # Получить список страниц блога, которые являются потомками этой страницы
        pages = SpecialtyPage.objects.live().descendant_of(self)
        return pages

class ProfessionsPage(Page):
    body = StreamField([
    ('carousel', blocks.StreamBlock([
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
    ]) )
    ], use_json_field=True, blank=True,verbose_name='Фотографии слайдера')
    related_document = models.ForeignKey(
        'wagtaildocs.Document',verbose_name='Учебная программа', blank=True, null=True,
         on_delete=models.SET_NULL, related_name='+'
    )
    time = models.CharField(max_length=250, blank=True,verbose_name='Сроки обучения')
    p = RichTextField(blank=True, verbose_name='Текст описания')
    html = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True, verbose_name='Видео', null=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        DocumentChooserPanel('related_document'),
        FieldPanel('time'),
        FieldPanel('p'),
        StreamFieldPanel('html')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('p'),
        ]


class ProfessionsIndexPage(Page):
    intro = RichTextField(blank=True)
    html = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True,null=True )

    content_panels = Page.content_panels + [
        StreamFieldPanel('html')
    ]
    @property
    def professions(self):
        # Получить список страниц блога, которые являются потомками этой страницы
        pages = ProfessionsPage.objects.live().descendant_of(self)
        return pages
        
