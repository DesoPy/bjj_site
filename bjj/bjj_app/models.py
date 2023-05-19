from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.news)


class NewsReaction(models.Model):
    LIKE = 'like'
    LOVE = 'love'
    HAHA = 'haha'
    WOW = 'wow'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (LOVE, 'Love'),
        (HAHA, 'Haha'),
        (WOW, 'Wow')
    ]
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='reactions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.news)

    def get_reaction_type_display(self):
        return dict(self.REACTION_CHOICES).get(self.reaction_type)


class Photo(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'Photo'
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo', kwargs={'photo_slug': self.slug})


class CommentPhoto(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ['-date']


class Trainer(models.Model):
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    contact_phone = models.CharField(max_length=20)
    information = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.full_name)


class Schedule(models.Model):
    WEEKDAYS_CHOICES = (
        ('monday', 'Понеділок'),
        ('tuesday', 'Вівторок'),
        ('wednesday', 'Середа'),
        ('thursday', 'Четвер'),
        ('friday', 'П\'ятниця'),
        ('saturday', 'Субота'),
        ('sunday', 'Неділя'),
    )

    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.CharField(max_length=9, choices=WEEKDAYS_CHOICES)
    forma = models.CharField(max_length=20)
    group = models.CharField(max_length=255)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.start_time} {self.end_time} {self.weekday} {self.forma} {self.group} {self.trainer}'

    class Meta:
        verbose_name = 'Schedule'
        # verbose_name_plural = 'Schedule'
        # ordering = ['weekday']
