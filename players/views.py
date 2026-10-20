from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum, Avg, Count, Max
from .models import Player, Club


class PlayerListView(ListView):
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'
    paginate_by = 20

    def get_queryset(self):
        qs = Player.objects.select_related('club', 'nationality')

        search = self.request.GET.get('search', '').strip()
        position = self.request.GET.get('position', '')
        sort = self.request.GET.get('sort', '-market_value')

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(club__name__icontains=search) |
                Q(nationality__name__icontains=search)
            )
        if position:
            qs = qs.filter(position=position)

        allowed_sorts = ['market_value', '-market_value', 'age', '-age',
                         'goals', '-goals', 'name', '-name']
        if sort in allowed_sorts:
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['positions'] = Player.POSITIONS
        ctx['current_search'] = self.request.GET.get('search', '')
        ctx['current_position'] = self.request.GET.get('position', '')
        ctx['current_sort'] = self.request.GET.get('sort', '-market_value')

        # Общая статистика по всем игрокам
        all_players = Player.objects.all()
        ctx['total_players'] = all_players.count()
        ctx['total_clubs'] = Club.objects.count()
        ctx['total_value'] = all_players.aggregate(s=Sum('market_value'))['s'] or 0
        ctx['avg_value'] = all_players.aggregate(a=Avg('market_value'))['a'] or 0
        ctx['top_player'] = all_players.order_by('-market_value').first()

        return ctx


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'

    def get_queryset(self):
        return Player.objects.select_related('club', 'nationality') \
                             .prefetch_related('transfers__to_club')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Похожие игроки: та же позиция, кроме текущего
        ctx['similar_players'] = Player.objects.filter(
            position=self.object.position
        ).exclude(pk=self.object.pk).order_by('-market_value')[:5]
        return ctx


class ClubDetailView(DetailView):
    model = Club
    template_name = 'players/club_detail.html'
    context_object_name = 'club'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        players = self.object.players.order_by('-market_value')
        ctx['players'] = players
        ctx['total_value'] = players.aggregate(s=Sum('market_value'))['s'] or 0
        ctx['players_count'] = players.count()
        return ctx