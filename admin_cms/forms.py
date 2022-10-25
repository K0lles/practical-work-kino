from django.forms import modelform_factory, Select, CheckboxInput, modelformset_factory, FileInput, TextInput, \
    RadioSelect

from banner.models import MainTopBanner, MainTopBannerPhoto, NewsBanner, NewsBannerPhoto, BackgroundBanner

main_top_banner_form_factory = modelform_factory(MainTopBanner, fields=('turned_on', 'turning_speed'),
                                                 widgets={
                                                     'turning_speed': Select(attrs={'class': 'form-control'}),
                                                     'turned_on': CheckboxInput()
                                                 })

main_top_formset_factory = modelformset_factory(MainTopBannerPhoto, exclude=('main_top_banner',), extra=0,
                                                widgets={
                                                    'photo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
                                                    'url': TextInput(
                                                        attrs={'class': 'form-control', 'placeholder': 'URL'}),
                                                    'text': TextInput(
                                                        attrs={'class': 'form-control', 'placeholder': 'текст'})
                                                }, can_delete=True)

news_banner_form_factory = modelform_factory(NewsBanner, fields=('turning_speed', 'turned_on'),
                                             widgets={
                                                 'turning_speed': Select(attrs={'class': 'form-control'})
                                             })

news_banner_formset_factory = modelformset_factory(NewsBannerPhoto,
                                                   fields=('photo', 'url'),
                                                   extra=0,
                                                   widgets={
                                                       'photo': FileInput(
                                                           attrs={'onchange': 'loadFile(event, this.id)'}),
                                                       'url': TextInput(
                                                           attrs={'class': 'form-control', 'placeholder': 'URL'})
                                                   },
                                                   can_delete=True)

background_banner_form_factory = modelform_factory(BackgroundBanner, fields=('photo', 'background'),
                                                   widgets={
                                                       'background': RadioSelect(attrs={'class': 'form-control'}),
                                                       'photo': FileInput(
                                                           attrs={'onchange': 'loadFile(event, this.id)'})
                                                   })