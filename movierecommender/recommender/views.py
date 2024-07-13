from django.shortcuts import render
from joblib import load
import difflib

# Load data
movies_data = load('./savedModels/movies_data.joblib')
similarity = load('./savedModels/similarity.joblib')

def recommender(user_movie):
    movies = movies_data['original_title'].to_list()
    matches = difflib.get_close_matches(user_movie, movies,cutoff=0.7)
    input_words = user_movie.split()
    close_match = [match for match in matches if all(word in match.lower() for word in input_words)]
    if not close_match:
        return "No close matches found for the movie."
    close_match = close_match[0]
    try:
        idx = movies_data[movies_data['title'] == close_match].index.values[0]
    except IndexError:
        return "Index not found for the close match."
    
    similar_scores = list(enumerate(similarity[idx]))
    sorting = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for i, movie in enumerate(sorting[:9]):
        idx = movie[0]
        title = movies_data.loc[idx, 'original_title']
        recommendations.append(title)
    
    return recommendations

# Views
def home(request):
    return render(request, 'index.html')

def result(request):
    if 'user_movie' in request.GET:
        user_movie = request.GET['user_movie'].strip().lower() 
        recommendations = recommender(user_movie)
        return render(request, 'result.html', {'results': recommendations})
    else:
        return render(request, 'result.html', {'results': None})
