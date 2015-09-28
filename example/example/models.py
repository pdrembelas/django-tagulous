"""
Models for example Tagulous app

Based on the usage examples in the documentation:
    http://radiac.net/projects/django-tagulous/documentation/usage/
"""
from django.db import models
import tagulous.models


class Skill(tagulous.models.TagTreeModel):
    class TagMeta:
        initial = [
            'Python/Django',
            'Python/Flask',
            'JavaScript/JQuery',
            'JavaScript/Angular.js',
            'Linux/nginx',
            'Linux/uwsgi',
        ]
        space_delimiter = False
        autocomplete_view = 'person_skills_autocomplete'


class Person(models.Model):
    name = models.CharField(max_length=255)
    title = tagulous.models.SingleTagField(initial="Mr, Mrs")
    skills = tagulous.models.TagField(Skill)
    hobbies = tagulous.models.TagField(
        initial="eating, coding, gaming",
        force_lowercase=True,
        blank=True,
    )
    class Meta:
        verbose_name_plural = 'people'
