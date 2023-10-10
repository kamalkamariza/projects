import csv
from io import TextIOWrapper
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match
from .forms import UploadCSVForm, EditMatchForm, AddMatchForm

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_reader = csv.reader(TextIOWrapper(csv_file))

            for row in csv_reader:
                home_team_name, home_score, away_team_name, away_score = row
                home_team, created = Team.objects.get_or_create(name=home_team_name)
                away_team, created = Team.objects.get_or_create(name=away_team_name)
                
                match = Match.objects.create(
                    home_team=home_team,
                    away_team=away_team,
                    home_score=int(home_score),
                    away_score=int(away_score)
                )
                match.update_team_points()

            return redirect('display_rankings')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def display_rankings(request):
    teams = Team.objects.order_by('-points', 'name')
    return render(request, 'display_rankings.html', {'teams': teams})

def add_match(request):
    if request.method == 'POST':
        form = AddMatchForm(request.POST)
        if form.is_valid():
            # Create or retrieve home and away teams
            home_team, created = Team.objects.get_or_create(name=form.cleaned_data['home_team_name'])
            away_team, created = Team.objects.get_or_create(name=form.cleaned_data['away_team_name'])
            
            # Create the match with the corresponding teams
            match = Match(
                home_team=home_team,
                away_team=away_team,
                home_score=form.cleaned_data['home_score'],
                away_score=form.cleaned_data['away_score']
            )
            match.update_team_points()
            return redirect('match_list')
    else:
        form = AddMatchForm()
    
    return render(request, 'add_match.html', {'form': form})

def edit_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        form = EditMatchForm(request.POST, instance=match)
        if form.is_valid():
            match.update_team_points()
            return redirect('match_list')
    else:
        form = EditMatchForm(instance=match)
    
    return render(request, 'edit_match.html', {'form': form, 'match': match})

def delete_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.delete_match()
    return redirect('match_list')

def match_list(request):
    matches = Match.objects.all()  # Query the database to fetch all matches
    return render(request, 'match_list.html', {'matches': matches})