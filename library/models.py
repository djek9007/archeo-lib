from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from django.utils import timezone
from dynamic_filenames import FilePattern
from image_cropping import ImageRatioField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _

page_file_item = FilePattern(filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}')


class CategoryLibrary(MPTTModel):
    """Класс модели категорий книг"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("url", max_length=50, unique=True, blank=True, null=True)
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
        verbose_name = "Категория библиотеки"
        verbose_name_plural = "Категории библиотеки"


class KeyBook(models.Model):
    """Модель тегов"""
    name = models.CharField('Название ключевого слова', max_length=100, unique=True)
    slug = models.SlugField('url', max_length=80, unique=True)
    in_main = models.BooleanField("отображать на главной странице?", default=False)
    published = models.BooleanField("отображать?", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"


class Author(models.Model):
    """Модель авторов"""
    name = models.CharField(verbose_name="ФИО автора", max_length=200)
    slug = models.SlugField('url', max_length=80, unique=True)
    image = models.ImageField('Фото автора', upload_to=page_file_item, blank=True, null=True)
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
    published = models.BooleanField("Отображать?", default=True)
    views = models.PositiveIntegerField("Просмотрено", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class YearBook(models.Model):
    """Модель годов"""
    year = models.CharField(verbose_name='Год', unique=True, max_length=4)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Годы"


class Editor(models.Model):
    """Модель годов"""
    name = models.CharField(verbose_name='Редактор', unique=True, max_length=255)
    slug = models.SlugField('url', max_length=80, unique=True)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Редактор"
        verbose_name_plural = "Редакторы"


class Book(models.Model):
    category = models.ForeignKey(CategoryLibrary, verbose_name='Категория', on_delete=models.CASCADE)
    year = models.ForeignKey(YearBook, verbose_name='Год', on_delete=models.CASCADE)
    editor = models.ManyToManyField(Editor, verbose_name='Редактор')
    author = models.ManyToManyField(Author, verbose_name='Автор/(ы)')
    title = models.CharField(verbose_name='Название', max_length=255)
    page = models.PositiveIntegerField(verbose_name='Страницы')
    description = RichTextField(_("Описание книги"), blank=True, null=True)
    file = models.FileField(verbose_name='Файл для чтение pdf', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    keyword = models.ManyToManyField(verbose_name='Ключевые слова')
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Библиотека"
        verbose_name_plural = "Библиотека"
