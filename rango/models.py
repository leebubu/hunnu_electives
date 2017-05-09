# coding: UTF-8
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from DjangoUeditor.commands import UEditorButtonCommand,UEditorComboCommand
from DjangoUeditor.commands import UEditorEventHandler

class Campus(models.Model):
    name = models.CharField(max_length=128)
    name_ch = models.CharField(max_length=100)
    #views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
	
    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Campus, self).save(*args, **kwargs)

    def __unicode__(self):      
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=128)
    title_ch = models.CharField(max_length=100, blank=True)
    #views = models.IntegerField(default=0)
    #likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    campus = models.ForeignKey(Campus)
	
    def save(self, *args, **kwargs):
                self.slug = slugify(self.title)
                super(Subject, self).save(*args, **kwargs)
    def __unicode__(self):      
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_ch = models.CharField(max_length=100, blank=True)
    #views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
	
    subject = models.ForeignKey(Subject)

    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

    def __unicode__(self):  
        return self.name


'''		
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
'''
		
class CategoryUserLikes(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)

class Answers(models.Model):
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)
	
    content = models.CharField(max_length=10000, blank=True)
    post_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content
		
class BaiduEditor(models.Model):
    content = UEditorField(u'', width='100%', height=300,
                     toolbars="full",
                     imagePath='Comment_images/%(basename)s_%(datetime)s.%(extname)s',
                     filePath='Comment_files/%(basename)s_%(datetime)s.%(extname)s',
                     upload_settings={
                         "imageMaxSize": 1204000},
                     settings={},
                     command=None,
                     blank=True)

class AnswerUserLikes(models.Model):
    answer = models.ForeignKey(Answers)
    user = models.ForeignKey(User)
    time = models.DateTimeField()


class AnswerUserDislikes(models.Model):
    answer = models.ForeignKey(Answers)
    user = models.ForeignKey(User)
    time = models.DateTimeField()
	
