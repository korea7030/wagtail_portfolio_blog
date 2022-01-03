from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks


# Create your models here.
class BlogListingPage(RoutablePageMixin, Page):
    '''listing page lists all the blog detail pages'''
    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwirtes the default title'
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        '''Adding custom stuff to our context.'''
        context = super(BlogListingPage, self).get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        context['a_special_link'] = self.reverse_subpage('latest_posts')
        return context
    
    @route(r'^latest/?$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)


class BlogDetailPage(RoutablePageMixin, Page):
    template = 'blog/blog_detail_page.html'

    '''Blog detail page'''
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwirtes the default title'
    )

    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    content = StreamField(
        [
            ('title_and_text', blocks.TitleandTextBlock()),
            ('full_richtext', blocks.RichTextBlock()),
            ('simple_richtext', blocks.SimpleRichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]

