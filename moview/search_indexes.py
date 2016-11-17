from haystack import indexes
from moview.models import Movie

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
	title = indexes.CharField(document=True, model_attr='title')

	def get_model(self):
		return Movie

