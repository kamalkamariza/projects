from .models import Team, Match, HistoricalMatch
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class TeamModelTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', points=5)

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Test Team')

class MatchModelTestCase(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Test Team 1', points=0)
        self.team2 = Team.objects.create(name='Test Team 2', points=0)

    def test_update_team_points_win(self):
        match = Match.objects.create(home_team=self.team1, away_team=self.team2, home_score=2, away_score=1)
        match.update_team_points()
        
        self.assertEqual(self.team1.points, 3)
        self.assertEqual(self.team2.points, 0)

    def test_update_team_points_tie(self):
        match = Match.objects.create(home_team=self.team1, away_team=self.team2, home_score=1, away_score=1)
        match.update_team_points()
        
        self.assertEqual(self.team1.points, 1)
        self.assertEqual(self.team2.points, 1)

    def test_delete_match(self):
        match = Match.objects.create(home_team=self.team1, away_team=self.team2, home_score=1, away_score=2)
        match.update_team_points()
        match.delete_match()
        
        self.assertEqual(self.team1.points, 0)
        self.assertEqual(self.team2.points, 0)

    def test_update_match_differ_from_historical(self):
        match = Match.objects.create(home_team=self.team1, away_team=self.team2, home_score=1, away_score=2)
        historical_match = HistoricalMatch.objects.create(historical_match=match, home_team=self.team1.name, away_team=self.team2.name, historical_home_score=1, historical_away_score=2)
        match.update_team_points()
        historical_match.save()
        match.home_score = 2
        match.update_team_points([historical_match])
        
        self.assertEqual(self.team1.points, 1)
        self.assertEqual(self.team2.points, 1)

class HomeViewTestCase(TestCase):
    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class UploadCSVViewTestCase(TestCase):
    def test_upload_csv_view(self):
        csv_content = "Test Team 1,2,Test Team 2,1\nTest Team 3,1,Test Team 4,2\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"))

        url = reverse('upload_csv')
        response = self.client.post(url, {'csv_file': csv_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('display_rankings'))

        self.assertEqual(Team.objects.count(), 4)  
        self.assertEqual(Match.objects.count(), 2)

class DisplayRankingsViewTestCase(TestCase):
    def test_display_rankings_view(self):
        team1 = Team.objects.create(name='Test Team 1', points=10)
        team2 = Team.objects.create(name='Test Team 2', points=5)
        team3 = Team.objects.create(name='Test Team 3', points=15)

        url = reverse('display_rankings')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_rankings.html')

        teams_in_context = list(response.context['teams'])
        self.assertEqual(teams_in_context, [team3, team1, team2])

class MatchListViewTestCase(TestCase):
    def test_match_list_view(self):
        team1 = Team.objects.create(name='Test Team 1', points=10)
        team2 = Team.objects.create(name='Test Team 2', points=5)

        match1 = Match.objects.create(home_team=team1, away_team=team2, home_score=2, away_score=1)
        match2 = Match.objects.create(home_team=team2, away_team=team1, home_score=1, away_score=1)

        url = reverse('match_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'match_list.html')

        matches_in_context = list(response.context['matches'])
        self.assertEqual(matches_in_context, [match1, match2])

class AddMatchViewTestCase(TestCase):
    def test_add_match_view(self):
        url = reverse('add_match')

        form_data = {
            'home_team_name': 'Test Team 1',
            'away_team_name': 'Test Team 2',
            'home_score': 2,
            'away_score': 1,
        }

        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('match_list'))

        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(HistoricalMatch.objects.count(), 1)

class EditMatchViewTestCase(TestCase):
    def test_edit_match_view(self):
        team1 = Team.objects.create(name='Test Team 1', points=10)
        team2 = Team.objects.create(name='Test Team 2', points=5)
        match = Match.objects.create(home_team=team1, away_team=team2, home_score=2, away_score=1)
        match.update_team_points()
        historical_match = HistoricalMatch.objects.create(historical_match=match, home_team=team1.name, away_team=team2.name, historical_home_score=match.home_score, historical_away_score=match.away_score)
        historical_match.save()

        url = reverse('edit_match', args=[match.id])
        form_data = {
            'home_team': team1.id,
            'away_team': team2.id,
            'home_score': 3,
            'away_score': 2,
        }

        response = self.client.post(url, form_data)
        print("TEST", response.content.decode())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('match_list'))

        match.refresh_from_db()
        self.assertEqual(match.home_score, 3)
        self.assertEqual(match.away_score, 2)

class DeleteMatchViewTestCase(TestCase):
    def test_delete_match_view(self):
        team1 = Team.objects.create(name='Test Team 1', points=10)
        team2 = Team.objects.create(name='Test Team 2', points=5)
        match = Match.objects.create(home_team=team1, away_team=team2, home_score=2, away_score=1)

        url = reverse('delete_match', args=[match.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('match_list'))

        self.assertEqual(Match.objects.count(), 0)

