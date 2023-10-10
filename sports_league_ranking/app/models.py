from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    class Meta:
        app_label = 'app'

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    class Meta:
        app_label = 'app'

    def __str__(self):
        return f'{self.home_team} {self.home_score} - {self.away_score} {self.away_team}'

    def update_team_points(self, historical_match=None):
        historical_winner = None
        if historical_match:
            historical_match = historical_match[0]
            if historical_match.historical_home_score > historical_match.historical_away_score:
                historical_winner = historical_match.home_team
            elif historical_match.historical_home_score < historical_match.historical_away_score:
                historical_winner = historical_match.away_team
            else:
                historical_winner = 'tie-match'

        if self.home_score > self.away_score:
            self.home_team.points += 3
            if historical_winner == self.away_team.name:
                self.away_team.points -= 3
            elif historical_winner == 'tie-match':
                self.away_team.points -= 1
                self.home_team.points -= 1
        elif self.home_score < self.away_score:
            self.away_team.points += 3
            if historical_winner == self.home_team.name:
                self.home_team.points -= 3
            elif historical_winner == 'tie-match':
                self.away_team.points -= 1
                self.home_team.points -= 1
        else:
            if historical_winner == self.home_team.name:
                self.home_team.points -= 3
            elif historical_winner == self.away_team.name:
                self.away_team.points -= 3

            if not historical_winner == 'tie-match':
                self.home_team.points += 1
                self.away_team.points += 1

        if historical_match:
            historical_match.historical_home_score = self.home_score
            historical_match.historical_away_score = self.away_score
            historical_match.save()

        self.home_team.save()
        self.away_team.save()
        self.save()

    def delete_match(self):
        if self.home_score > self.away_score:
            self.home_team.points -= 3
        elif self.home_score < self.away_score:
            self.away_team.points -= 3
        elif self.home_team.points == self.away_team.points:
            self.home_team.points -= 1
            self.away_team.points -= 1

        self.home_team.save()
        self.away_team.save()
        self.delete()

class HistoricalMatch(models.Model):
    historical_match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='historical_matches')
    home_team = models.CharField(max_length=100, default='')
    away_team = models.CharField(max_length=100, default='')
    historical_home_score = models.IntegerField()
    historical_away_score = models.IntegerField()

    class Meta:
        app_label = 'app'