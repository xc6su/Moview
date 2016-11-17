import scipy.io
from ccf import SGD_Egreedy_Contextual

file = open(FILENAME, 'r')
context = scipy.io.mmread(file)

clf = SGD_Egreedy_Contextual()

"""
k = 25, context_dim = 5, context_feature = context, 
"""



# def temp(request):
# 	jsonFile = open(os.path.join(PROJECT_ROOT, 'movies.json'))
# 	ja = json.load(jsonFile)
# 	for jo in ja:
# 		movie = Movie(id=(int(jo['mid']) + 1), title=jo['title'], genre=jo['genres'], director=jo['director'], rating=(float(jo['rating']) / 2.), year=jo['year'], poster=jo['poster']
# 				, release_date=jo['release_date'], detail_poster=jo['detail_poster'], rate_cnt=jo['rate_cnt'], duration=jo['duration'], description=jo['description'])
# 		movie.save()

# def insertUser(request):
# 	userCnt = 669
# 	temp = "test"
# 	field = "@test.com"
# 	password = "a"
# 	for i in range(1, userCnt):
# 		username = temp + str(i)
# 		email = username + field
# 		User.objects.create_user(username, email, password, first_name=username, id=i)

# def insertMovieMat(request):
# 	contextF = open(os.path.join(PROJECT_ROOT, 'data/feature_vectors.dat'), 'rb')
# 	mmF = open(os.path.join(PROJECT_ROOT, 'data/item_vectors.dat'), 'rb')
# 	context = scipy.io.mmread(contextF)
# 	moviem = scipy.io.mmread(mmF)
# 	for i in range(1, len(context)):
# 		mat = MovieMatrix(movie=Movie.objects.get(pk=i), vector=moviem[i].tolist(), context_feature=context[i].tolist())
# 		mat.save()

def insertUM(request):
	umf = open(os.path.join(PROJECT_ROOT, 'data/user_vectors.dat'), 'rb')
	um = scipy.io.mmread(umf)
	for i in range(1, len(um)):
		m = UserMatrix(user=User.objects.get(pk=i), vector=um[i].tolist())
		m.save()