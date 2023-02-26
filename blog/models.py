from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.
from dynamic_filenames import FilePattern
from image_cropping import ImageRatioField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

page_file_item = FilePattern(filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}')


class Category(MPTTModel):
    """Класс модели категорий сетей"""
    name = models.CharField("Название", max_length=100)
    slug = models.CharField("url", max_length=50, unique=True, blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    published = models.BooleanField("Отображать?", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    """Класс модели поста"""
    category = TreeForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Заголовок", max_length=500)
    slug = models.SlugField("url", max_length=50, unique=True)
    image = models.ImageField('Главное фото', upload_to=page_file_item, blank=True, null=True)
    list_page_cropping = ImageRatioField('image', '122x134')
    detail_page_cropping = ImageRatioField('image', '254x355')
    description = RichTextField(_("Описание автора"), blank=True, null=True)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )

    published = models.BooleanField("Опубликовать?", default=True)
    enable_post_date = models.BooleanField(verbose_name='Показывать дату поста?', default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title


class Pages(models.Model):
    """Страницы"""
    title = models.CharField(_("Заголовок"), max_length=250)
    slug = models.SlugField("ссылка", max_length=50, unique=True)
    image = models.ImageField("фотография", upload_to=page_file_item, blank=True, null=True)
    text = RichTextField(_("Текст"), blank=True, null=True)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        _("Дата редактирования"),
        auto_now=True,
        blank=True,
        null=True
    )
    published = models.BooleanField(_("Опубликовать?"), default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"