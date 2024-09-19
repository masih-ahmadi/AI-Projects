import pdfplumber
import re
from django.core.management.base import BaseCommand
from modules.models import Module

class Command(BaseCommand):
    help = 'Extracts modules from the provided PDF and stores them in the database'

    def handle(self, *args, **kwargs):
        pdf_path = 'path_to_your_pdf/Module_Catalogue_M.Sc.AI-Engineering.pdf'

        def extract_modules_from_pdf(pdf_path):
            with pdfplumber.open(pdf_path) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()
            
            modules = re.split(r'\n\d{4}\s', text)[1:]
            for module in modules:
                lines = module.split('\n')
                module_name = lines[0].strip()
                ects_search = re.search(r'(\d{1,2})\s*ECTS', module)
                credits = int(ects_search.group(1)) if ects_search else None
                description_search = re.search(r'(Inhalt|Course content)(.*?)(Studien|Assessment)', module, re.DOTALL)
                description = description_search.group(2).strip() if description_search else ''

                Module.objects.create(module_name=module_name, credits=credits, description=description)
        
        extract_modules_from_pdf(pdf_path)
        self.stdout.write(self.style.SUCCESS('Modules extracted and stored successfully.'))
