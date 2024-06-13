from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class ChampionshipIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    subpage_types = ['championships.ChampionshipPage']

class ChampionshipPage(Page, ClusterableModel):
    CHAMPIONSHIP_TYPES = [
        ('professional', 'Профессионалы'),
        ('abilimpics', 'Абилимпикс'),
    ]

    type = models.CharField(
        max_length=20,
        choices=CHAMPIONSHIP_TYPES,
        default='professional',
    )
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('type'),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('image'),
        InlinePanel('participation_years', label="История участия"),
    ]

    parent_page_types = ['championships.ChampionshipIndexPage']
    subpage_types = []

class ParticipationYear(ClusterableModel):
    page = ParentalKey(ChampionshipPage, on_delete=models.CASCADE, related_name='participation_years')
    year = models.IntegerField("Год участия")
    championship_name = models.CharField(max_length=255, blank=True, null=True)

    panels = [
        FieldPanel('year'),
        FieldPanel('championship_name'),
        InlinePanel('competences', label="Компетенции"),
    ]

    def __str__(self):
        return f"{self.year} - {self.championship_name}"

class Competence(models.Model):
    participation_year = ParentalKey(ParticipationYear, on_delete=models.CASCADE, related_name='competences')
    competence = models.CharField(max_length=255)
    result = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('competence'),
        FieldPanel('result'),
    ]

    def __str__(self):
        return self.competence

class ChampionshipParticipationPage(Page):
    parent_page_types = ['championships.ChampionshipPage']
    subpage_types = []

    content_panels = Page.content_panels + []
