from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import User, Bunk

# Views

# Main view
class MainView(generic.ListView):
	context_object_name = 'latest_bunks_list'
	template_name = 'bunky/main.html'

	def get_queryset(self):
		"""Returns the latest 100 Bunks!"""
		return Bunk.objects.filter(time__lte=timezone.now()).order_by('-time')[:100]

# Find view
def find(request):
	# If the request is a post request:
	if request.POST:

		#Extracts the response
		response = request.POST['username']

		# Handles if there is no response
		if not response:
			return render(request, 'bunky/find.html', {
				'error_message': 'Haha, very funny. You need to actually enter a username, doofus.'})

		# Extracts users with the given username and takes the length of that set
		users = User.objects.filter(username=response)
		length = len(users)

		# Handles if there are multiple users of the same username (BUG)
		if length > 1:
			return render(request, 'bunky/find.html', {
				'error_message': 'So uh... this is awkward... There are kinda sorta... multiple users with that username...'})
		# Handles if there is no user with given username
		elif length < 1:
			return render(request, 'bunky/find.html', {
				'error_message': 'Did you even know if there was someone with that username? Because there definitely is not...'})

		# Returns the homepage of the extracted user
		return HttpResponseRedirect(reverse('bunky:home', args=(users[0].id,)))

	# If the request is not a post request (Visiting from MAIN view)
	else:

		return render(request, 'bunky/find.html')

# Home view
def home(request, user_id):
	# Extracts the user object
	user = get_object_or_404(User, pk=user_id)
	# Combines sets of the bunks that contain user as the bunker or bunkee, sorts the set, and takes the first 100
	bunks = (Bunk.objects.filter(to_user=user).union(Bunk.objects.filter(from_user=user))).order_by('-time')[:100]

	return render(request, 'bunky/home.html', {
		'bunks': bunks,
		'user': user})

# Bunk view
def bunk(request, user_id):
	# First confirms that the user exists
	user = get_object_or_404(User, pk=user_id)
	# If the request is a post request:
	if request.POST:

		#Extracts the response
		response = request.POST['username']

		# Handles if there is no response
		if not response:
			return render(request, 'bunky/bunk.html', {
				'error_message': 'Haha, very funny. You need to actually enter a username, doofus.',
				'user' :user})

		# Handles if there are multiple users of the same username (BUG)
		users = User.objects.filter(username=response)
		length = len(users)

		# Handles if there are multiple users of the same username (BUG)
		if length > 1:
			return render(request, 'bunky/bunk.html', {
				'error_message': 'So uh... this is awkward... There are kinda sorta... multiple users with that username...',
				'user': user})
		# Handles if there is no user with given username
		elif length < 1:
			return render(request, 'bunky/bunk.html', {
				'error_message': 'Did you even know if there was someone with that username? Because there definitely is not...',
				'user': user})

		# Creates a new bunk from the extracted information and saves it
		bunk = Bunk(from_user=user, to_user=users[0], time=timezone.now())
		bunk.save()
		return HttpResponseRedirect(reverse('bunky:bunked', args=(bunk.id,)))

	# If the request is not a post request (Visiting from HOME view)
	else:

		return render(request, 'bunky/bunk.html', {
			'user': user})

# Bunk confirmation view
class BunkedView(generic.DetailView):
	model = Bunk
	template_name = 'bunky/bunked.html'

