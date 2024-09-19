import pdfplumber
import re
import pandas as pd
from django.core.management.base import BaseCommand
from modules.models import Module

class Command(BaseCommand):
    help = 'Extract modules from PDF and save them to the database'

    def handle(self, *args, **kwargs):
        pdf_path = 'data/Module_Catalogue_M.Sc.AI-Engineering.pdf'  # Update this to the correct path
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        
        modules = re.split(r'\n\d{4}\s', text)[1:]
        for module in modules:
            module_info = {}
            lines = module.split('\n')
            module_name = lines[0].strip()
            
            ects_search = re.search(r'(\d{1,2})\s*Credits', module, re.DOTALL)
            credits = int(ects_search.group(1)) if ects_search else 0
    
            
            # Extract Description (from 'Inhalt' to 'Assessment')
            description_search = re.search(r'(Inhalt|Course content)(.*?)(Studien|Assessment)', module, re.DOTALL)
            description = description_search.group(2).strip() if description_search else ''
            
            # Extract Lecturer (Dozent)
            lecturer_search = re.search(r'(Dozent|Lecturer)(.*?)(Sprache|Language)', module, re.DOTALL)
            lecturer = lecturer_search.group(2).strip() if lecturer_search else 'Not found'
            
            # Extract Learning Outcomes (Lernziele)
            learning_outcomes_search = re.search(r'(Angestrebte Lernergebnisse|Learning outcomes)(.*?)(Inhalt|Course content)', module, re.DOTALL)
            learning_outcomes = learning_outcomes_search.group(2).strip() if learning_outcomes_search else 'Not found'
            
            # Extract Assessment (Studien und Prüfungsleistungen)
            assessment_search = re.search(r'(Studien|Assessment)(.*?)(Medienformen|Media used)', module, re.DOTALL)
            assessment = assessment_search.group(2).strip() if assessment_search else 'Not found'
            
            if credits != 0:
            # Print extracted module info
                Module.objects.create(
                    module_name=module_name,
                    description=description,
                    credits=credits,
                    professor=lecturer,
                    outcomes=learning_outcomes,
                    assessment=assessment
                )

        
        self.stdout.write(self.style.SUCCESS('Modules have been extracted and stored in the database.'))
