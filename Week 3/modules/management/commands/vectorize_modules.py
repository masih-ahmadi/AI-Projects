import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from django.core.management.base import BaseCommand
from modules.models import Module

class Command(BaseCommand):
    help = 'Vectorize module descriptions and store them for querying'

    def handle(self, *args, **kwargs):
        modules = Module.objects.all()
        descriptions = [
    f"{module.module_name} {module.professor} {module.credits} {module.assessment} {module.outcomes} {module.description}"
    for module in modules
]
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(descriptions)
        
        with open('module_vectors.pkl', 'wb') as f:
            pickle.dump((X, vectorizer, list(modules.values())), f)

        self.stdout.write(self.style.SUCCESS('Modules have been vectorized and stored.'))
