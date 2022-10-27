from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, \
    UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
from django.forms import modelform_factory, modelformset_factory, ModelForm, CharField, Form, BooleanField, ChoiceField, \
    FileField
from modeltranslation.forms import TranslationModelForm
from django.forms.widgets import FileInput, Textarea, TextInput, Select, DateTimeInput, NumberInput, \
    RadioSelect, PasswordInput, CheckboxInput
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from user.models import SimpleUser
from event.models import *
from cinema.models import *
from movie.models import Movie
from page.models import *
from banner.models import *

hall_formset_factory = modelformset_factory(Hall, fields=('number', 'created_at'), extra=0,
                                            widgets={
                                                'number': TextInput(attrs={'readonly': True}),
                                                'created_at': DateTimeInput(attrs={'readonly': True})
                                            }, can_delete=True)

photo_formset_factory = modelformset_factory(Photo, fields=('photo',), extra=0,
                                             widgets={
                                                 'photo': FileInput(attrs={'onchange': 'loadFile(event, this.id)',
                                                                           'accept': 'image/*'}),
                                             },
                                             can_delete=True)


class CinemaForm(TranslationModelForm):

    class Meta:
        model = Cinema
        exclude = ('gallery', 'seo')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'condition': Textarea(attrs={'class': 'form-control'}),
            'logo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
            'banner_photo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'})
        }


seo_form_factory = modelform_factory(SEO, fields=('url', 'title', 'keyword', 'seo_description'),
                                     widgets={
                                         'url': TextInput(attrs={'class': 'form-control'}),
                                         'title': TextInput(attrs={'class': 'form-control'}),
                                         'keyword': TextInput(attrs={'class': 'form-control'}),
                                         'seo_description': Textarea(attrs={'class': 'form-control'})
                                     })


class HallForm(TranslationModelForm):
    class Meta:
        model = Hall
        exclude = ('cinema_id', 'gallery', 'created_at', 'row_amount', 'seat_amount', 'seo', )
        widgets = {
            'number': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'scheme': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
            'banner_photo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
        }


class MovieForm(TranslationModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['description'].widget = Textarea(attrs={'class': 'form-control'})
        self.fields['main_photo'].widget = FileInput(attrs={'onchange': 'loadFile(event, this.id)'})
        self.fields['trailer_url'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['type_2D'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['type_IMAX'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['type_3D'].widget = CheckboxInput(attrs={'class': 'form-check-input'})

    class Meta:
        model = Movie
        exclude = ['gallery', 'seo']


class EventForm(TranslationModelForm):

    class Meta:
        model = Event
        exclude = ('seo', 'created_at', 'gallery', 'type')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'logo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
            'url': TextInput(attrs={'class': 'form-control'}),

        }


main_page_form_factory = modelform_factory(MainPage, exclude=('seo', 'created_at'),
                                           widgets={
                                               'phone_number_first': PhoneNumberInternationalFallbackWidget(
                                                   attrs={'class': 'form-control'}
                                               ),
                                               'phone_number_second': PhoneNumberInternationalFallbackWidget(
                                                   attrs={'class': 'form-control'}
                                               ),
                                               'seo_text': Textarea(attrs={'class': 'form-control'}),
                                           })


def func_contact_formset_factory(extra_forms):
    return modelformset_factory(Contacts, exclude=('seo',), extra=extra_forms,
                                widgets={
                                    'cinema_name': TextInput(attrs={'class': 'form-control'}),
                                    'address': Textarea(attrs={'class': 'form-control'}),
                                    'coordinates': TextInput(attrs={'class': 'form-control'}),
                                    'logo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'})
                                })


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

user_form_factory = modelform_factory(SimpleUser,
                                      fields='__all__',
                                      widgets={
                                          'name': TextInput(attrs={'class': 'form-control'}),
                                          'surname': TextInput(attrs={'class': 'form-control'}),
                                          'alias': TextInput(attrs={'class': 'form-control'}),
                                          'birthday': TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Дата народження'}),
                                          'phone_number': TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Номер телефону'}),
                                          'card_number': NumberInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Номер банківської картки'}),
                                          'language': RadioSelect(attrs={'class': 'form-check-input'}),
                                          'sex': RadioSelect(attrs={'class': 'form-check-input'}),
                                          'city': TextInput(attrs={'class': 'form-control'}),
                                          'password1': PasswordInput(attrs={'class': 'form-control'})
                                      })


class UserFormUpdate(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sex'].empty_label = None
        self.fields['birthday'].input_formats = ['%d.%m.%Y']
        self.fields['password'].required = False
        # del self.fields['password1']

    password_repeat = CharField(widget=PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Повторіть пароль'}), required=False)

    class Meta:
        model = SimpleUser
        exclude = ['date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'surname': TextInput(attrs={'class': 'form-control'}),
            'alias': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'birthday': TextInput(attrs={'class': 'form-control',
                                         'placeholder': 'Дата народження'}),
            'phone_number': TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Номер телефону'}),
            'card_number': NumberInput(attrs={'class': 'form-control',
                                              'placeholder': 'Номер банківської картки'}),
            'language': RadioSelect(attrs={'class': 'form-check-input'}),
            'sex': RadioSelect(attrs={'class': 'form-check-input'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новий пароль'}),
        }

    def clean(self):
        cleaned_data = super(UserFormUpdate, self).clean()
        card_number = cleaned_data.get('card_number')

        if len(card_number) < 16 or not card_number.isnumeric():
            self.add_error('card_number', 'Incorrect card number. Check it writing!')

        if cleaned_data.get('password'):
            validate_password(cleaned_data.get('password'), password_validators=(MinimumLengthValidator(),
                                                                                 UserAttributeSimilarityValidator(),
                                                                                 CommonPasswordValidator(),
                                                                                 NumericPasswordValidator()))

        if cleaned_data.get('password') != cleaned_data.get('password_repeat') and cleaned_data.get('password'):
            self.add_error('password', "Passwords must match. Check the validity of entered passwords!")

        return cleaned_data


pages_formset_factory = modelformset_factory(Page, fields=('name', 'created_at', 'status'), extra=0, can_delete=True)


class PageCreateForm(TranslationModelForm):
    class Meta:
        model = Page
        exclude = ('gallery', 'seo', 'created_at', 'type')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'main_photo': FileInput(attrs={'onchange': 'loadFile(event, this.id)'}),
            'status': CheckboxInput()
        }


class SendMail(Form):
    user_email_list = CharField(required=False, widget=Textarea())
    send_to_current_user = BooleanField(required=False)

    CHOICES = (
        (True, 'Всім користувачам'),
        (False, 'Вибраним користувачам'),
    )

    all_users = ChoiceField(choices=CHOICES, required=True, widget=RadioSelect())
    users = CharField(widget=Textarea, required=False)