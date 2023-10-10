import csv
from io import TextIOWrapper
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, HistoricalMatch, AppUser
from .forms import UploadCSVForm, EditMatchForm, AddMatchForm, UserCreationForm, UserLoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'display_rankings.html')

@login_required(login_url='login')
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

                historical_match = HistoricalMatch.objects.create(
                    historical_match=match,
                    home_team=home_team.name,
                    away_team=away_team.name,
                    historical_home_score=match.home_score,
                    historical_away_score=match.away_score
                )
                historical_match.save()


            return redirect('display_rankings')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def display_rankings(request):
    teams = Team.objects.order_by('-points', 'name')
    return render(request, 'display_rankings.html', {'teams': teams})

@login_required(login_url='login')
def add_match(request):
    if request.method == 'POST':
        form = AddMatchForm(request.POST)
        if form.is_valid():
            home_team, created = Team.objects.get_or_create(name=form.cleaned_data['home_team_name'])
            away_team, created = Team.objects.get_or_create(name=form.cleaned_data['away_team_name'])
            
            match = Match(
                home_team=home_team,
                away_team=away_team,
                home_score=form.cleaned_data['home_score'],
                away_score=form.cleaned_data['away_score']
            )
            match.update_team_points()

            historical_match = HistoricalMatch.objects.create(
                historical_match=match,
                home_team=home_team.name,
                away_team=away_team.name,
                historical_home_score=match.home_score,
                historical_away_score=match.away_score
            )
            historical_match.save()
            return redirect('match_list')
    else:
        form = AddMatchForm()
    
    return render(request, 'add_match.html', {'form': form})

@login_required(login_url='login')
def edit_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        form = EditMatchForm(request.POST, instance=match)
        if form.is_valid():
            historical_match = HistoricalMatch.objects.filter(historical_match=match)
            match.update_team_points(historical_match)
            return redirect('match_list')
    else:
        form = EditMatchForm(instance=match)
    
    return render(request, 'edit_match.html', {'form': form, 'match': match})

@login_required(login_url='login')
def delete_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.delete_match()
    return redirect('match_list')

def match_list(request):
    matches = Match.objects.all()
    return render(request, 'match_list.html', {'matches': matches})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = get_object_or_404(AppUser, username=username)
            
            if user is not None and password == user.password:
                login(request, user)
                return redirect('home')  # Redirect to the home page or any other page
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
