from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		
		if form.is_valid() and p_form.is_valid():
			form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		form = UserUpdateForm(instance=request.user)

	context = {
		'u_form' : form,
	}

	return render(request, 'users/profile.html', context)
