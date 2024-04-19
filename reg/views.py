from django.shortcuts import render, redirect

from register.reg.form import SignUpForm


def homepage(request):
    pass


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    pass


def dashboard(request):
    pass
