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
        return f"{self.home_team.name} {self.home_score} vs. {self.away_team.name} {self.away_score}"
    
    def update_team_points(self):
        if self.home_score > self.away_score:
            self.home_team.points += 3
        elif self.home_score < self.away_score:
            self.away_team.points += 3
        else:
            self.home_team.points += 1
            self.away_team.points += 1

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
