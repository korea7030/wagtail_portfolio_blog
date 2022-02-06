from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleandTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & Text'
        form_classname = 'text_and_title'


class CardBlock(blocks.StructBlock):
    '''Cards with image and text and button(s)'''
    title = blocks.CharBlock(required=True, help_text='Add your title')
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=True, max_length=40)),
                ('text', blocks.TextBlock(required=True, max_length=200)),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_url', blocks.URLBlock(required=False,
                  help_text='If the button page above is selected, that will be used first.')),
            ]
        )
    )

    class Meta:
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff Cards'
        form_classname = 'staff card'

    

class RichTextBlock(blocks.RichTextBlock):
    ''' richtext with all the features, '''
    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'doc-full'
        label = 'Full RichText'
        form_classname = 'rich_text'


class SimpleRichTextBlock(blocks.RichTextBlock):
    ''' richtext without (limited) all the features, '''

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link',
        ]

    class Meta:
        template = 'streams/simple_richtext_block.html'
        icon = 'edit'
        label = 'Simple RichText'
        form_classname = 'simple_rich_text'


class CTABlock(blocks.StructBlock):
    '''A simple call to action section.'''
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta:
        template = 'streams/cta_block.html'
        icon = 'placeholder'
        label = 'Call to Action'
        form_classname = 'call_to_action'


class LinkStructValue(blocks.StructValue):
    '''Additional logic for our urls'''
    from blog.models import BlogDetailPage
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')

        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        
        return None


class ButtonBlock(blocks.StructBlock):
    '''An external or internal URL.'''
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the page')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:
        template = 'streams/button_block.html'
        icon = 'placeholder'
        label = 'single button'
        form_classname = 'single button'
        value_class = LinkStructValue


class TimelineBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100)
    text = blocks.TextBlock()
    date = blocks.DateBlock()

    class Meta:
        icon = "placeholder"
        template = "streams/timeline_block.html"
