from django.db import models
from django.contrib.postgres.fields import JSONField,ArrayField
from django.contrib.auth import get_user_model
from django.contrib.postgres import fields
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json
# Create your models here.


class Authors(models.Model):
    name = models.TextField(unique = True)
    done = models.BooleanField()

class Article(models.Model):
    title = models.TextField()
    type = models.TextField()

    authors = models.ManyToManyField(Authors)
    identifiers = JSONField()

    keywords = ArrayField(base_field=models.CharField(max_length=20),null=True,blank=True)

    year = models.IntegerField()
    source = models.TextField()
    publisher = models.TextField()
    id = models.CharField(max_length=50,unique=True,primary_key=True)
    pdf = models.URLField(default=None,null=True,max_length=350)
    link = models.URLField()

    reader_count = models.IntegerField()
    reader_count_by_academic_status = JSONField()
    reader_count_by_subject_area = JSONField()
    reader_count_by_country = JSONField()

    # reader_count_by_academic_status = models.TextField()
    # reader_count_by_subject_area = models.TextField()
    # reader_count_by_country = models.TextField()

    def get_json(self):
        json_ = {
            "title":self.title,
            "type":self.type,
            "authors":list(self.authors.all().values_list("name",flat=True)),
            "source":self.source,
            "publisher":self.publisher,
            "pdf":self.pdf,
            "link":self.link,
            "reader_count":self.reader_count,
            "reader_count_by_academic_status":self.reader_count_by_academic_status,
            "reader_count_by_subject_area":self.reader_count_by_subject_area,
            "reader_count_by_country":self.reader_count_by_country
        }
        return json_

    def get_pdf_url(self):
        validator = URLValidator()
        try:
            validator(self.pdf)
            return self.pdf
        except ValidationError:
            if "doi" in self.identifiers: return f"https://dx.doi.org/{self.identifiers['doi']}"
            return None

    def get_issn(self):
        if "issn" in self.identifiers:
             return f"https://portal.issn.org/api/search?search[]=MUST=allissnbis={self.identifiers['issn'][:4]}-{self.identifiers['issn'][4:]}"

        return None

    def get_doi(self):
        if "doi" in self.identifiers:
             return f"https://dx.doi.org/{self.identifiers['doi']}"

        return None

    def get_total(self):
        count = 0
        for review in self.review_set.all():
            count+=review.rating

        return int(count)


class Review(models.Model):
    rating = models.IntegerField(choices=((-1,-1),(1,1)))
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(),on_delete=models.CASCADE)



class Library(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

class Comment(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, models.DO_NOTHING)
    user = models.ForeignKey(get_user_model(), models.DO_NOTHING)
