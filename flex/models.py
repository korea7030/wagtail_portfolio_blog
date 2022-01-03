from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from streams.blocks import RichTextBlock, SimpleRichTextBlock, TitleandTextBlock, CardBlock, CTABlock, ButtonBlock


class FlexPage(Page):
    template = 'flex/flex_page.html'

    subtitle = models.CharField(max_length=100, null=True, blank=True)
    content = StreamField(
        [
            ('title_and_text', TitleandTextBlock()),
            ('full_richtext', RichTextBlock()),
            ('simple_richtext', SimpleRichTextBlock()),
            ('cards', CardBlock()),
            ('cta', CTABlock()),
            ('button', ButtonBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Flex Pages'
