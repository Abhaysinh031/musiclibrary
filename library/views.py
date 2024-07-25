from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Music, Folder, Favorite
from .forms import FolderForm, MusicForm



def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MusicForm(request.POST, request.FILES)
            if form.is_valid():
                music = form.save(commit=False)
                music.user = request.user  # Assuming you have a user field in your Music model
                music.save()
                return redirect('home')  # Redirect to home page after successful upload
        else:
            form = MusicForm()
    else:
        form = None

    music_list = Music.objects.all()  # Retrieve all music tracks to display

    return render(request, 'library/home.html', {
        'form': form,
        'music_list': music_list,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'library/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'library/login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user = request.user
    folders = user.folder_set.all()
    favorite_music = Favorite.objects.filter(user=user).first()
    if request.method == 'POST':
        music_id = request.POST.get('music_id')
        music = get_object_or_404(Music, id=music_id)
        if favorite_music:
            favorite_music.music.add(music)
        else:
            favorite_music = Favorite(user=user)
            favorite_music.save()
            favorite_music.music.add(music)
        return redirect('profile')
    return render(request, 'library/profile.html', {
        'folders': folders,
        'favorite_music': favorite_music.music.all() if favorite_music else [],
    })


@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('profile')
    else:
        form = FolderForm()
    return render(request, 'library/create_folder.html', {'form': form})


@login_required
def manage_folder(request, folder_id=None):
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    else:
        folder = Folder(user=request.user)

    if request.method == 'POST':
        folder_form = FolderForm(request.POST, instance=folder)
        music_form = MusicForm(request.POST, request.FILES)
        if folder_form.is_valid():
            folder = folder_form.save(commit=False)
            folder.user = request.user
            folder.save()
            files = request.FILES.getlist('file')
            for file in files:
                music = Music(file=file, title=request.POST.get('title'), artist=request.POST.get('artist'), genre=request.POST.get('genre'))
                music.save()
                folder.music.add(music)
            folder.save()
            return redirect('profile')
    else:
        folder_form = FolderForm(instance=folder)
        music_form = MusicForm()

    return render(request, 'library/manage_folder.html', {
        'folder_form': folder_form,
        'music_form': music_form,
        'folder': folder if folder_id else None,
    })

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == 'POST':
        folder.delete()
        return redirect('home')
    return render(request, 'library/confirm_delete.html', {'object': folder, 'type': 'folder'})

@login_required
def delete_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if request.method == 'POST':
        music.delete()
        return redirect('home')
    return render(request, 'library/confirm_delete.html', {'object': music, 'type': 'music'})


@login_required
def favorites(request):
    user = request.user
    favorite = Favorite.objects.filter(user=user).first()
    music_list = favorite.music.all() if favorite else []
    folders_list = favorite.folders.all() if favorite else []
    
    if request.method == 'POST':
        if 'music_id' in request.POST:
            music_id = request.POST.get('music_id')
            music = get_object_or_404(Music, id=music_id)
            if favorite:
                favorite.music.remove(music)
        elif 'folder_id' in request.POST:
            folder_id = request.POST.get('folder_id')
            folder = get_object_or_404(Folder, id=folder_id)
            if favorite:
                favorite.folders.remove(folder)
        return redirect('favorites')
    
    return render(request, 'library/favorites.html', {'music_list': music_list, 'folders_list': folders_list})
@login_required
def add_folder_to_favorites(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    
    if folder not in favorite.folders.all():
        favorite.folders.add(folder)
        favorite.save()
    
    return redirect('favorites')
