from django.db import models
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    founded = models.PositiveIntegerField(blank=True, null=True)  

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('club_detail', args=[self.pk])


class Player(models.Model):
    POSITIONS = [
        ('GK', 'Вратарь'),
        ('DF', 'Защитник'),
        ('MF', 'Полузащитник'),
        ('FW', 'Нападающий'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    position = models.CharField(max_length=2, choices=POSITIONS, verbose_name='Позиция')
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Гражданство')
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='players', verbose_name='Клуб')
    photo = models.ImageField(upload_to='players/', blank=True, null=True, verbose_name='Фото')
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Игровой номер')
    market_value = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='Цена (млн €)')

    matches = models.PositiveIntegerField(default=0, verbose_name='Матчи')
    goals = models.PositiveIntegerField(default=0, verbose_name='Голы')
    assists = models.PositiveIntegerField(default=0, verbose_name='Ассисты')
    achievements = models.TextField(blank=True, verbose_name='Достижения',
                                    help_text='Каждое достижение с новой строки')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ['-market_value']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player_detail', args=[self.pk])

    @property
    def achievements_list(self):
        return [a.strip() for a in self.achievements.split('\n') if a.strip()]


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transfers')
    from_club = models.CharField(max_length=100, blank=True, verbose_name='Из клуба')
    to_club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name='transfers_in', verbose_name='В клуб')
    price = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='Сумма (млн €)')
    year = models.PositiveIntegerField(verbose_name='Год')

    class Meta:
        verbose_name = 'Трансфер'
        verbose_name_plural = 'Трансферы'
        ordering = ['-year']

    def __str__(self):
        return f'{self.player.name} → {self.to_club} ({self.year})'