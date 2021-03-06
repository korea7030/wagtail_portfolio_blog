from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page, ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


from streams.blocks import RichTextBlock, SimpleRichTextBlock, TitleandTextBlock, CardBlock, CTABlock


class BlogAuthorsOrderable(Orderable):
    '''This allows us to select one or more blug authors from snippets'''
    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel('author'),
    ]


class BlogAuthor(models.Model):
    '''Blog author for snippets'''
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('image'),
            ],
            heading='Name and Image'
        ),
        MultiFieldPanel(
            [
                FieldPanel('website'),
            ],
            heading='Links'
        )
    ]

    def __str__(self):
        '''String repr of this class.'''
        return self.name
    
    class Meta:
        verbose_name = 'Blog Author'


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    ''' Blog category for a snippet. '''
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


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
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 6)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['authors'] = BlogAuthor.objects.all()
        context['categories'] = BlogCategory.objects.all()
        return context
    
    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_posts'),
                'lastmod': (self.last_published_at or self.latest_revision_created_at),
                'priority': 0.9
            }
        )
        return sitemap

class BlogDetailPage(RoutablePageMixin, Page):
    template = 'blog/blog_detail_page.html'

    '''Blog detail page'''
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwirtes the default title'
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    categories = ParentalManyToManyField('blog.BlogCategory')

    content = StreamField(
        [
            ('title_and_text', TitleandTextBlock()),
            ('full_richtext', RichTextBlock()),
            ('simple_richtext', SimpleRichTextBlock()),
            ('cards', CardBlock()),
            ('cta', CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
        ], heading='Author(s)'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories'),
        StreamFieldPanel('content'),
    ]


# First sub classed blog post page
class ArticleBlogPage(BlogDetailPage):
    '''A subclassed blog post page for article'''
    template = 'blog/article_blog_page.html'
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        ImageChooserPanel('intro_image'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
        ], heading='Author(s)'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories'),
        StreamFieldPanel('content'),
    ]


# Second subclassed page
class VideoBlogPage(BlogDetailPage):
    '''A video subclassed page.'''
    template = 'blog/video_blog_page.html'
    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
        ], heading='Author(s)'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories'),
        FieldPanel('youtube_video_id'),
        StreamFieldPanel('content'),
    ]