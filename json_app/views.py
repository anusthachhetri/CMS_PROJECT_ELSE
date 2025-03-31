import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient
from .models import JSONFile
from django.http import HttpResponse
from django.urls import reverse
from bson.json_util import dumps
from urllib.parse import quote_plus
import datetime


#adding home view##############################
#############################################################################

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
@login_required
def home(request):
    return render(request, 'home.html')  # for our home template



#####################scrapper tool#######################################################
######################################################################################3

def scraper_tool(request):
    #tags = ["h1","h4","em", "h2", "h3", "p", "span", "a", "div", "li", "ul", "ol", "table", "tr", "td", "th"]
   
    #print("✅ View is being executed!")  # Debugging
    #print("Tags passed to template:", tags)  # Debugging
   
    return render(request, "scraper.html")
 
 
import asyncio
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
 
 
def extract_tag_sequences(html_content, tag_sequence):
    """
    Extract structured data based on a sequential list of HTML tags.
    Each tag in the sequence will be paired with its corresponding content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_data = []
    elements = soup.find_all(tag_sequence[0])
 
    for element in elements:
        entry = {tag_sequence[0]: element.get_text(strip=True)}
 
        # Traverse subsequent tags in sequence
        for next_tag in tag_sequence[1:]:
            next_element = element.find_next(next_tag)
            entry[next_tag] = next_element.get_text(strip=True) if next_element else None
            element = next_element if next_element else element
 
        extracted_data.append(entry)
 
    return extracted_data
 
 
async def scrape_page_content(url, tag_sequence):
    """
    Asynchronous scraping function using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            page_source = await page.content()
            return extract_tag_sequences(page_source, tag_sequence)
        except Exception as e:
            return [{"Error": str(e)}]
        finally:
            await browser.close()
 
 
def scraper_view(request):
    if request.method == "POST":
        url = request.POST.get("url")
        tags = request.POST.getlist("tags")  # Get selected tags as a list
 
        if url and tags:
            result = asyncio.run(scrape_page_content(url, tags))
            df = pd.DataFrame(result)
            csv_file = df.to_csv(index=False)
 
            return JsonResponse({"data": result, "csv": csv_file})
 
    return render(request, "scraper.html")

#########################ending here########################################################


#######################################scrapper tool 2 for awardieee#####################################
###################################################################################

# import asyncio
# import pandas as pd
# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from bs4 import BeautifulSoup
# from playwright.async_api import async_playwright


# def extract_tag_sequences(html_content, tag_sequence):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     extracted_data = []
#     elements = soup.find_all(tag_sequence[0])

#     for element in elements:
#         entry = {tag_sequence[0]: element.get_text(strip=True)}

#         for next_tag in tag_sequence[1:]:
#             next_element = element.find_next(next_tag)
#             entry[next_tag] = next_element.get_text(strip=True) if next_element else None
#             element = next_element if next_element else element

#         extracted_data.append(entry)

#     return extracted_data


# async def scrape_page_content(url, tag_sequence):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         try:
#             page = await browser.new_page()
#             await page.goto(url, timeout=60000)

#             initial_data = extract_tag_sequences(await page.content(), tag_sequence)
#             return initial_data
#         except Exception as e:
#             return [{"Error": str(e)}]
#         finally:
#             await browser.close()


# def web_scraper_view(request):
#     if request.method == "POST":
#         url = request.POST.get("url")
#         tag_sequence = request.POST.getlist("tags[]")

#         if not url or not tag_sequence:
#             return JsonResponse({"error": "Please provide a valid URL and select tags."}, status=400)

#         scraped_data = asyncio.run(scrape_page_content(url, tag_sequence))

#         if "download" in request.POST:
#             df = pd.DataFrame(scraped_data)
#             response = HttpResponse(df.to_csv(index=False), content_type="text/csv")
#             response["Content-Disposition"] = 'attachment; filename="scraped_content.csv"'
#             return response

#         return JsonResponse({"data": scraped_data}, safe=False)

#     return render(request, "web_scraper.html")

import asyncio
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from asgiref.sync import async_to_sync
import validators

def extracts_tags_sequences(html_content, tag_sequence):
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_data = []

    for tag in tag_sequence:
        elements = soup.find_all(tag)
        for element in elements:
            extracted_data.append({tag: element.get_text(strip=True)})

    return extracted_data if extracted_data else [{"Message": "No data found for selected tags"}]

async def scrp_pag_content(url, tag_sequence):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            scraped_data = extracts_tags_sequences(await page.content(), tag_sequence)
            return scraped_data
        except Exception as e:
            return [{"Error": str(e)}]
        finally:
            await browser.close()

def web_scraper_view(request):
    if request.method == "POST":
        url = request.POST.get("url")
        tag_sequence = request.POST.getlist("tags[]")

        if not url or not tag_sequence or not validators.url(url):
            return JsonResponse({"error": "Invalid input."}, status=400)

        scraped_data = async_to_sync(scrp_pag_content)(url, tag_sequence)

        if "download" in request.POST:
            df = pd.DataFrame(scraped_data)
            response = HttpResponse(df.to_csv(index=False), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="scraped_content.csv"'
            return response

        return JsonResponse({"data": scraped_data}, safe=False)

    return render(request, "web_scraper.html")


###################################ending here#######################################################


###############ASJC CODE MATCHER MODIFIED###########################
# from django.shortcuts import render
# from sentence_transformers import SentenceTransformer, util
# import torch

# # Load Sentence Transformers model for semantic similarity
# sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# # ASJC mapping dictionary
# asjc_mapping = {
#     "1000": "General",
#     "1100": "Agricultural and Biological Sciences (all)",
#     "1101": "Agricultural and Biological Sciences (miscellaneous)",
#     "1102": "Agronomy and Crop Science",
#     "1103": "Animal Science and Zoology",
#     "1104": "Aquatic Science",
#     "1105": "Ecology, Behavior and Systematics",
#     "1106": "Food Science",
#     "1107": "Forestry",
#     "1108": "Horticulture",
#     "1109": "Insect Science",
#     "1110": "Plant Science",
#     "1111": "Soil Science",
#     "1200": "Arts and Humanities (all)",
#     "1201": "Arts and Humanities (miscellaneous)",
#     "1202": "History",
#     "1203": "Language and Linguistics",
#     "1204": "Archaeology",
#     "1205": "Classics",
#     "1206": "Conservation",
#     "1207": "History and Philosophy of Science",
#     "1208": "Literature and Literary Theory",
#     "1209": "Museology",
#     "1210": "Music",
#     "1211": "Philosophy",
#     "1212": "Religious Studies",
#     "1213": "Visual Arts and Performing Arts",
#     "1302": "Ageing",
#     "1303": "Biochemistry",
#     "1304": "Biophysics",
#     "1305": "Biotechnology",
#     "1306": "Cancer Research",
#     "1307": "Cell Biology",
#     "1308": "Clinical Biochemistry",
#     "1309": "Developmental Biology",
#     "1310": "Endocrinology",
#     "1311": "Genetics",
#     "1312": "Molecular Biology",
#     "1313": "Molecular Medicine",
#     "1314": "Physiology",
#     "1315": "Structural Biology",
#     "1402": "Accounting",
#     "1403": "Business and International Management",
#     "1404": "Management Information Systems",
#     "1405": "Management of Technology and Innovation",
#     "1406": "Business",
#     "1407": "Organizational Behavior and Human Resource Management",
#     "1408": "Strategy and Management",
#     "1409": "Tourism",
#     "1410": "Industrial Relations",
#     "1500": "Chemical Engineering (all)",
#     "1501": "Chemical Engineering (miscellaneous)",
#     "1502": "Bioengineering",
#     "1503": "Catalysis",
#     "1504": "Chemical Health and Safety",
#     "1505": "Colloid and Surface Chemistry",
#     "1506": "Filtration and Separation",
#     "1507": "Fluid Flow and Transfer Processes",
#     "1508": "Process Chemistry and Technology",
#     "1600": "Chemistry (all)",
#     "1601": "Chemistry (miscellaneous)",
#     "1602": "Analytical Chemistry",
#     "1603": "Electrochemistry",
#     "1604": "Inorganic Chemistry",
#     "1605": "Organic Chemistry",
#     "1606": "Physical and Theoretical Chemistry",
#     "1607": "Spectroscopy",
#     "1700": "Computer Science (all)",
#     "1701": "Computer Science (miscellaneous)",
#     "1702": "Artificial Intelligence",
#     "1703": "Computational Theory and Mathematics",
#     "1704": "Computer Graphics and Computer-Aided Design",
#     "1705": "Computer Networks and Communications",
#     "1706": "Computer Science Applications",
#     "1707": "Computer Vision and Pattern Recognition",
#     "1708": "Hardware and Architecture",
#     "1709": "Human-Computer Interaction",
#     "1710": "Information Systems",
#     "1711": "Signal Processing",
#     "1712": "Software",
#     "1800": "Decision Sciences (all)",
#     "1801": "Decision Sciences (miscellaneous)",
#     "1802": "Information Systems and Management",
#     "1803": "Management Science and Operations Research",
#     "1804": "Statistics",
#     "1900": "Earth and Planetary Sciences (all)",
#     "1901": "Earth and Planetary Sciences (miscellaneous)",
#     "1902": "Atmospheric Science",
#     "1903": "Computers in Earth Sciences",
#     "1904": "Earth-Surface Processes",
#     "1905": "Economic Geology",
#     "1906": "Geochemistry and Petrology",
#     "1907": "Geology",
#     "1908": "Geophysics",
#     "1909": "Geotechnical Engineering and Engineering Geology",
#     "1910": "Oceanography",
#     "1911": "Palaeontology",
#     "1912": "Space and Planetary Science",
#     "1913": "Stratigraphy",
#     "2002": "Economics and Econometrics",
#     "2003": "Finance",
#     "2100": "Energy (all)",
#     "2101": "Energy (miscellaneous)",
#     "2102": "Energy Engineering and Power Technology",
#     "2103": "Fuel Technology",
#     "2104": "Nuclear Energy and Engineering",
#     "2105": "Renewable Energy",
#     "2200": "Engineering (all)",
#     "2201": "Engineering (miscellaneous)",
#     "2202": "Aerospace Engineering",
#     "2203": "Automotive Engineering",
#     "2204": "Biomedical Engineering",
#     "2205": "Civil and Structural Engineering",
#     "2206": "Computational Mechanics",
#     "2207": "Control and Systems Engineering",
#     "2208": "Electrical and Electronic Engineering",
#     "2209": "Industrial and Manufacturing Engineering",
#     "2210": "Mechanical Engineering",
#     "2211": "Mechanics of Materials",
#     "2212": "Ocean Engineering",
#     "2213": "Safety, Reliability and Quality",
#     "2214": "Media Technology",
#     "2215": "Building and Construction",
#     "2216": "Architecture",
#     "2300": "Environmental Science (all)",
#     "2301": "Environmental Science (miscellaneous)",
#     "2302": "Ecological Modelling",
#     "2303": "Ecology",
#     "2304": "Environmental Chemistry",
#     "2305": "Environmental Engineering",
#     "2306": "Global and Planetary Change",
#     "2308": "Management Policy and Law",
#     "2309": "Nature and Landscape Conservation",
#     "2310": "Pollution",
#     "2311": "Waste Management and Disposal",
#     "2312": "Water Science and Technology",
#     "2400": "Immunology and Microbiology (all)",
#     "2401": "Immunology and Microbiology (miscellaneous)",
#     "2402": "Applied Microbiology and Biotechnology",
#     "2403": "Immunology",
#     "2404": "Microbiology",
#     "2405": "Parasitology",
#     "2406": "Virology",
#     "2500": "Materials Science (all)",
#     "2501": "Materials Science (miscellaneous)",
#     "2502": "Biomaterials",
#     "2503": "Ceramics and Composites",
#     "2505": "Materials Chemistry",
#     "2506": "Metals and Alloys",
#     "2507": "Polymers and Plastics",
#     "2600": "Mathematics (all)",
#     "2601": "Mathematics (miscellaneous)",
#     "2602": "Algebra and Number Theory",
#     "2603": "Analysis",
#     "2604": "Applied Mathematics",
#     "2605": "Computational Mathematics",
#     "2606": "Control and Optimization",
#     "2607": "Discrete Mathematics and Combinatorics",
#     "2608": "Geometry and Topology",
#     "2609": "Logic",
#     "2610": "Mathematical Physics",
#     "2611": "Modelling and Simulation",
#     "2612": "Numerical Analysis",
#     "2613": "Statistics and Probability",
#     "2614": "Theoretical Computer Science",
#     "2700": "Medicine (all)",
#     "2701": "Medicine (miscellaneous)",
#     "2702": "Anatomy",
#     "2703": "Anesthesiology and Pain Medicine",
#     "2705": "Cardiology and Cardiovascular Medicine",
#     "2706": "Critical Care and Intensive Care Medicine",
#     "2707": "Complementary and Alternative Medicine",
#     "2708": "Dermatology",
#     "2709": "Drug Guides",
#     "2710": "Embryology",
#     "2711": "Emergency Medicine",
#     "2713": "Epidemiology",
#     "2714": "Family Practice",
#     "2715": "Gastroenterology",
#     "2716": "Genetics (clinical)",
#     "2717": "Geriatrics and Gerontology",
#     "2718": "Health Informatics",
#     "2719": "Health Policy",
#     "2720": "Hematology",
#     "2721": "Hepatology",
#     "2722": "Histology",
#     "2723": "Immunology and Allergy",
#     "2724": "Internal Medicine",
#     "2725": "Infectious Diseases",
#     "2726": "Microbiology (medical)",
#     "2727": "Nephrology",
#     "2728": "Clinical Neurology",
#     "2729": "Obstetrics and Gynaecology",
#     "2730": "Oncology",
#     "2731": "Ophthalmology",
#     "2732": "Orthopedics and Sports Medicine",
#     "2733": "Otorhinolaryngology",
#     "2734": "Pathology and Forensic Medicine",
#     "2735": "Pediatrics and Child Health",
#     "2736": "Pharmacology (medical)",
#     "2737": "Physiology (medical)",
#     "2738": "Psychiatry and Mental Health",
#     "2739": "Public Health",
#     "2740": "Pulmonary and Respiratory Medicine",
#     "2741": "Radiology Nuclear Medicine and Imaging",
#     "2742": "Rehabilitation",
#     "2743": "Reproductive Medicine",
#     "2745": "Rheumatology",
#     "2746": "Surgery",
#     "2747": "Transplantation",
#     "2748": "Urology",
#     "2800": "Neuroscience (all)",
#     "2801": "Neuroscience (miscellaneous)",
#     "2802": "Behavioral Neuroscience",
#     "2803": "Biological Psychiatry",
#     "2804": "Cellular and Molecular Neuroscience",
#     "2805": "Cognitive Neuroscience",
#     "2806": "Developmental Neuroscience",
#     "2807": "Endocrine and Autonomic Systems",
#     "2808": "Neurology",
#     "2809": "Sensory Systems",
#     "2900": "Nursing (all)",
#     "2901": "Nursing (miscellaneous)",
#     "2902": "Advanced and Specialised Nursing",
#     "2903": "Assessment and Diagnosis",
#     "2904": "Care Planning",
#     "2905": "Community and Home Care",
#     "2906": "Critical Care",
#     "2907": "Emergency",
#     "2908": "Fundamentals and Skills",
#     "2909": "Gerontology",
#     "2911": "Leadership and Management",
#     "2912": "LPN and LVN",
#     "2913": "Maternity and Midwifery",
#     "2914": "Medical–Surgical",
#     "2915": "Nurse Assisting",
#     "2916": "Nutrition and Dietetics",
#     "2917": "Oncology (nursing)",
#     "2918": "Pathophysiology",
#     "2919": "Pediatrics",
#     "2920": "Pharmacology (nursing)",
#     "2921": "Phychiatric Mental Health",
#     "2922": "Research and Theory",
#     "2923": "Review and Exam Preparation",
#     "3002": "Drug Discovery",
#     "3003": "Pharmaceutical Science",
#     "3004": "Pharmacology",
#     "3005": "Toxicology",
#     "3100": "Physics and Astronomy (all)",
#     "3101": "Physics and Astronomy (miscellaneous)",
#     "3102": "Acoustics and Ultrasonics",
#     "3103": "Astronomy and Astrophysics",
#     "3104": "Condensed Matter Physics",
#     "3105": "Instrumentation",
#     "3106": "Nuclear and High Energy Physics",
#     "3107": "Atomic and Molecular Physics",
#     "3108": "Radiation",
#     "3109": "Statistical and Nonlinear Physics",
#     "3110": "Surfaces and Interfaces",
#     "3200": "Psychology (all)",
#     "3201": "Psychology (miscellaneous)",
#     "3202": "Applied Psychology",
#     "3203": "Clinical Psychology",
#     "3204": "Developmental and Educational Psychology",
#     "3205": "Experimental and Cognitive Psychology",
#     "3206": "Neuropsychology and Physiological Psychology",
#     "3207": "Social Psychology",
#     "3300": "Social Sciences (all)",
#     "3301": "Social Sciences (miscellaneous)",
#     "3302": "Archaeology",
#     "3303": "Development",
#     "3304": "Education",
#     "3305": "Geography",
#     "3306": "Health (social science)",
#     "3307": "Human Factors and Ergonomics",
#     "3308": "Law",
#     "3309": "Library and Information Sciences",
#     "3310": "Linguistics and Language",
#     "3311": "Safety Research",
#     "3312": "Sociology and Political Science",
#     "3313": "Transportation",
#     "3314": "Anthropology",
#     "3315": "Communication",
#     "3316": "Cultural Studies",
#     "3317": "Demography",
#     "3318": "Gender Studies",
#     "3319": "Life-span and Life-course Studies",
#     "3320": "Political Science and International Relations",
#     "3321": "Public Administration",
#     "3322": "Urban Studies",
#     "3400": "Veterinary (all)",
#     "3401": "Veterinary (miscellaneous)",
#     "3402": "Equine",
#     "3403": "Food Animals",
#     "3404": "Small Animals",
#     "3500": "Dentistry (all)",
#     "3501": "Dentistry (miscellaneous)",
#     "3502": "Dental Assisting",
#     "3503": "Dental Hygiene",
#     "3504": "Oral Surgery",
#     "3505": "Orthodontics",
#     "3506": "Periodontics",
#     "3600": "Health Professions (all)",
#     "3601": "Health Professions (miscellaneous)",
#     "3602": "Chiropractics",
#     "3603": "Complementary and Manual Therapy",
#     "3604": "Emergency Medical Services",
#     "3605": "Health Information Management",
#     "3606": "Medical Assisting and Transcription",
#     "3607": "Medical Laboratory Technology",
#     "3608": "Medical Terminology",
#     "3609": "Occupational Therapy",
#     "3610": "Optometry",
#     "3611": "Pharmacy",
#     "3613": "Podiatry",
#     "3614": "Radiological and Ultrasound Technology",
#     "3615": "Respiratory Care",
#     "3616": "Speech and Hearing",
#     # Add more categories as needed...
# }

# # Precompute ASJC embeddings
# asjc_embeddings = {code: sbert_model.encode(category, convert_to_tensor=True) for code, category in asjc_mapping.items()}

# def match_asjc_codes(text):
#     """Matches input text with ASJC codes based on similarity."""
#     if not text.strip():
#         return []

#     input_embedding = sbert_model.encode(text, convert_to_tensor=True)
#     scores = []

#     for code, category_embedding in asjc_embeddings.items():
#         similarity = util.pytorch_cos_sim(input_embedding, category_embedding).item()
#         scores.append((code, asjc_mapping[code], similarity))

#     # Sort by similarity (highest first)
#     scores.sort(key=lambda x: x[2], reverse=True)

#     # Return top 3-5 matches dynamically
#     if len(scores) > 3 and scores[3][2] > 0.65:
#         return scores[:5] if len(scores) > 4 and scores[4][2] > 0.6 else scores[:4]
    
#     return scores[:3]

# def asjc_matcher_view(request):
#     """Django view to handle ASJC code matching."""
#     matched_codes = []
#     input_text = ""

#     if request.method == "POST":
#         input_text = request.POST.get("text", "")
#         matched_codes = match_asjc_codes(input_text)

#     return render(request, "asjc_matcher.html", {"matched_codes": matched_codes, "input_text": input_text})



import json
import pandas as pd
import spacy
import torch
from django.shortcuts import render
from django.http import JsonResponse
from sentence_transformers import SentenceTransformer, util

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load Sentence Transformers model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# ASJC Mapping Dictionary
asjc_mapping = {
     "1000": "General",
    "1100": "Agricultural and Biological Sciences (all)",
    "1101": "Agricultural and Biological Sciences (miscellaneous)",
    "1102": "Agronomy and Crop Science",
    "1103": "Animal Science and Zoology",
    "1104": "Aquatic Science",
    "1105": "Ecology, Behavior and Systematics",
    "1106": "Food Science",
    "1107": "Forestry",
    "1108": "Horticulture",
    "1109": "Insect Science",
    "1110": "Plant Science",
    "1111": "Soil Science",
    "1200": "Arts and Humanities (all)",
    "1201": "Arts and Humanities (miscellaneous)",
    "1202": "History",
    "1203": "Language and Linguistics",
    "1204": "Archaeology",
    "1205": "Classics",
    "1206": "Conservation",
    "1207": "History and Philosophy of Science",
    "1208": "Literature and Literary Theory",
    "1209": "Museology",
    "1210": "Music",
    "1211": "Philosophy",
    "1212": "Religious Studies",
    "1213": "Visual Arts and Performing Arts",
    "1302": "Ageing",
    "1303": "Biochemistry",
    "1304": "Biophysics",
    "1305": "Biotechnology",
    "1306": "Cancer Research",
    "1307": "Cell Biology",
    "1308": "Clinical Biochemistry",
    "1309": "Developmental Biology",
    "1310": "Endocrinology",
    "1311": "Genetics",
    "1312": "Molecular Biology",
    "1313": "Molecular Medicine",
    "1314": "Physiology",
    "1315": "Structural Biology",
    "1402": "Accounting",
    "1403": "Business and International Management",
    "1404": "Management Information Systems",
    "1405": "Management of Technology and Innovation",
    "1406": "Business",
    "1407": "Organizational Behavior and Human Resource Management",
    "1408": "Strategy and Management",
    "1409": "Tourism",
    "1410": "Industrial Relations",
    "1500": "Chemical Engineering (all)",
    "1501": "Chemical Engineering (miscellaneous)",
    "1502": "Bioengineering",
    "1503": "Catalysis",
    "1504": "Chemical Health and Safety",
    "1505": "Colloid and Surface Chemistry",
    "1506": "Filtration and Separation",
    "1507": "Fluid Flow and Transfer Processes",
    "1508": "Process Chemistry and Technology",
    "1600": "Chemistry (all)",
    "1601": "Chemistry (miscellaneous)",
    "1602": "Analytical Chemistry",
    "1603": "Electrochemistry",
    "1604": "Inorganic Chemistry",
    "1605": "Organic Chemistry",
    "1606": "Physical and Theoretical Chemistry",
    "1607": "Spectroscopy",
    "1700": "Computer Science (all)",
    "1701": "Computer Science (miscellaneous)",
    "1702": "Artificial Intelligence",
    "1703": "Computational Theory and Mathematics",
    "1704": "Computer Graphics and Computer-Aided Design",
    "1705": "Computer Networks and Communications",
    "1706": "Computer Science Applications",
    "1707": "Computer Vision and Pattern Recognition",
    "1708": "Hardware and Architecture",
    "1709": "Human-Computer Interaction",
    "1710": "Information Systems",
    "1711": "Signal Processing",
    "1712": "Software",
    "1800": "Decision Sciences (all)",
    "1801": "Decision Sciences (miscellaneous)",
    "1802": "Information Systems and Management",
    "1803": "Management Science and Operations Research",
    "1804": "Statistics",
    "1900": "Earth and Planetary Sciences (all)",
    "1901": "Earth and Planetary Sciences (miscellaneous)",
    "1902": "Atmospheric Science",
    "1903": "Computers in Earth Sciences",
    "1904": "Earth-Surface Processes",
    "1905": "Economic Geology",
    "1906": "Geochemistry and Petrology",
    "1907": "Geology",
    "1908": "Geophysics",
    "1909": "Geotechnical Engineering and Engineering Geology",
    "1910": "Oceanography",
    "1911": "Palaeontology",
    "1912": "Space and Planetary Science",
    "1913": "Stratigraphy",
    "2002": "Economics and Econometrics",
    "2003": "Finance",
    "2100": "Energy (all)",
    "2101": "Energy (miscellaneous)",
    "2102": "Energy Engineering and Power Technology",
    "2103": "Fuel Technology",
    "2104": "Nuclear Energy and Engineering",
    "2105": "Renewable Energy",
    "2200": "Engineering (all)",
    "2201": "Engineering (miscellaneous)",
    "2202": "Aerospace Engineering",
    "2203": "Automotive Engineering",
    "2204": "Biomedical Engineering",
    "2205": "Civil and Structural Engineering",
    "2206": "Computational Mechanics",
    "2207": "Control and Systems Engineering",
    "2208": "Electrical and Electronic Engineering",
    "2209": "Industrial and Manufacturing Engineering",
    "2210": "Mechanical Engineering",
    "2211": "Mechanics of Materials",
    "2212": "Ocean Engineering",
    "2213": "Safety, Reliability and Quality",
    "2214": "Media Technology",
    "2215": "Building and Construction",
    "2216": "Architecture",
    "2300": "Environmental Science (all)",
    "2301": "Environmental Science (miscellaneous)",
    "2302": "Ecological Modelling",
    "2303": "Ecology",
    "2304": "Environmental Chemistry",
    "2305": "Environmental Engineering",
    "2306": "Global and Planetary Change",
    "2308": "Management Policy and Law",
    "2309": "Nature and Landscape Conservation",
    "2310": "Pollution",
    "2311": "Waste Management and Disposal",
    "2312": "Water Science and Technology",
    "2400": "Immunology and Microbiology (all)",
    "2401": "Immunology and Microbiology (miscellaneous)",
    "2402": "Applied Microbiology and Biotechnology",
    "2403": "Immunology",
    "2404": "Microbiology",
    "2405": "Parasitology",
    "2406": "Virology",
    "2500": "Materials Science (all)",
    "2501": "Materials Science (miscellaneous)",
    "2502": "Biomaterials",
    "2503": "Ceramics and Composites",
    "2505": "Materials Chemistry",
    "2506": "Metals and Alloys",
    "2507": "Polymers and Plastics",
    "2600": "Mathematics (all)",
    "2601": "Mathematics (miscellaneous)",
    "2602": "Algebra and Number Theory",
    "2603": "Analysis",
    "2604": "Applied Mathematics",
    "2605": "Computational Mathematics",
    "2606": "Control and Optimization",
    "2607": "Discrete Mathematics and Combinatorics",
    "2608": "Geometry and Topology",
    "2609": "Logic",
    "2610": "Mathematical Physics",
    "2611": "Modelling and Simulation",
    "2612": "Numerical Analysis",
    "2613": "Statistics and Probability",
    "2614": "Theoretical Computer Science",
    "2700": "Medicine (all)",
    "2701": "Medicine (miscellaneous)",
    "2702": "Anatomy",
    "2703": "Anesthesiology and Pain Medicine",
    "2705": "Cardiology and Cardiovascular Medicine",
    "2706": "Critical Care and Intensive Care Medicine",
    "2707": "Complementary and Alternative Medicine",
    "2708": "Dermatology",
    "2709": "Drug Guides",
    "2710": "Embryology",
    "2711": "Emergency Medicine",
    "2713": "Epidemiology",
    "2714": "Family Practice",
    "2715": "Gastroenterology",
    "2716": "Genetics (clinical)",
    "2717": "Geriatrics and Gerontology",
    "2718": "Health Informatics",
    "2719": "Health Policy",
    "2720": "Hematology",
    "2721": "Hepatology",
    "2722": "Histology",
    "2723": "Immunology and Allergy",
    "2724": "Internal Medicine",
    "2725": "Infectious Diseases",
    "2726": "Microbiology (medical)",
    "2727": "Nephrology",
    "2728": "Clinical Neurology",
    "2729": "Obstetrics and Gynaecology",
    "2730": "Oncology",
    "2731": "Ophthalmology",
    "2732": "Orthopedics and Sports Medicine",
    "2733": "Otorhinolaryngology",
    "2734": "Pathology and Forensic Medicine",
    "2735": "Pediatrics and Child Health",
    "2736": "Pharmacology (medical)",
    "2737": "Physiology (medical)",
    "2738": "Psychiatry and Mental Health",
    "2739": "Public Health",
    "2740": "Pulmonary and Respiratory Medicine",
    "2741": "Radiology Nuclear Medicine and Imaging",
    "2742": "Rehabilitation",
    "2743": "Reproductive Medicine",
    "2745": "Rheumatology",
    "2746": "Surgery",
    "2747": "Transplantation",
    "2748": "Urology",
    "2800": "Neuroscience (all)",
    "2801": "Neuroscience (miscellaneous)",
    "2802": "Behavioral Neuroscience",
    "2803": "Biological Psychiatry",
    "2804": "Cellular and Molecular Neuroscience",
    "2805": "Cognitive Neuroscience",
    "2806": "Developmental Neuroscience",
    "2807": "Endocrine and Autonomic Systems",
    "2808": "Neurology",
    "2809": "Sensory Systems",
    "2900": "Nursing (all)",
    "2901": "Nursing (miscellaneous)",
    "2902": "Advanced and Specialised Nursing",
    "2903": "Assessment and Diagnosis",
    "2904": "Care Planning",
    "2905": "Community and Home Care",
    "2906": "Critical Care",
    "2907": "Emergency",
    "2908": "Fundamentals and Skills",
    "2909": "Gerontology",
    "2911": "Leadership and Management",
    "2912": "LPN and LVN",
    "2913": "Maternity and Midwifery",
    "2914": "Medical–Surgical",
    "2915": "Nurse Assisting",
    "2916": "Nutrition and Dietetics",
    "2917": "Oncology (nursing)",
    "2918": "Pathophysiology",
    "2919": "Pediatrics",
    "2920": "Pharmacology (nursing)",
    "2921": "Phychiatric Mental Health",
    "2922": "Research and Theory",
    "2923": "Review and Exam Preparation",
    "3002": "Drug Discovery",
    "3003": "Pharmaceutical Science",
    "3004": "Pharmacology",
    "3005": "Toxicology",
    "3100": "Physics and Astronomy (all)",
    "3101": "Physics and Astronomy (miscellaneous)",
    "3102": "Acoustics and Ultrasonics",
    "3103": "Astronomy and Astrophysics",
    "3104": "Condensed Matter Physics",
    "3105": "Instrumentation",
    "3106": "Nuclear and High Energy Physics",
    "3107": "Atomic and Molecular Physics",
    "3108": "Radiation",
    "3109": "Statistical and Nonlinear Physics",
    "3110": "Surfaces and Interfaces",
    "3200": "Psychology (all)",
    "3201": "Psychology (miscellaneous)",
    "3202": "Applied Psychology",
    "3203": "Clinical Psychology",
    "3204": "Developmental and Educational Psychology",
    "3205": "Experimental and Cognitive Psychology",
    "3206": "Neuropsychology and Physiological Psychology",
    "3207": "Social Psychology",
    "3300": "Social Sciences (all)",
    "3301": "Social Sciences (miscellaneous)",
    "3302": "Archaeology",
    "3303": "Development",
    "3304": "Education",
    "3305": "Geography",
    "3306": "Health (social science)",
    "3307": "Human Factors and Ergonomics",
    "3308": "Law",
    "3309": "Library and Information Sciences",
    "3310": "Linguistics and Language",
    "3311": "Safety Research",
    "3312": "Sociology and Political Science",
    "3313": "Transportation",
    "3314": "Anthropology",
    "3315": "Communication",
    "3316": "Cultural Studies",
    "3317": "Demography",
    "3318": "Gender Studies",
    "3319": "Life-span and Life-course Studies",
    "3320": "Political Science and International Relations",
    "3321": "Public Administration",
    "3322": "Urban Studies",
    "3400": "Veterinary (all)",
    "3401": "Veterinary (miscellaneous)",
    "3402": "Equine",
    "3403": "Food Animals",
    "3404": "Small Animals",
    "3500": "Dentistry (all)",
    "3501": "Dentistry (miscellaneous)",
    "3502": "Dental Assisting",
    "3503": "Dental Hygiene",
    "3504": "Oral Surgery",
    "3505": "Orthodontics",
    "3506": "Periodontics",
    "3600": "Health Professions (all)",
    "3601": "Health Professions (miscellaneous)",
    "3602": "Chiropractics",
    "3603": "Complementary and Manual Therapy",
    "3604": "Emergency Medical Services",
    "3605": "Health Information Management",
    "3606": "Medical Assisting and Transcription",
    "3607": "Medical Laboratory Technology",
    "3608": "Medical Terminology",
    "3609": "Occupational Therapy",
    "3610": "Optometry",
    "3611": "Pharmacy",
    "3613": "Podiatry",
    "3614": "Radiological and Ultrasound Technology",
    "3615": "Respiratory Care",
    "3616": "Speech and Hearing",
    # Add more codes as needed...
}

# Precompute ASJC embeddings
asjc_embeddings = {code: sbert_model.encode(category, convert_to_tensor=True) for code, category in asjc_mapping.items()}

def match_asjc_codes(text):
    """Matches input text with ASJC codes based on similarity."""
    if not text.strip():
        return []

    input_embedding = sbert_model.encode(text, convert_to_tensor=True)
    scores = []

    for code, category_embedding in asjc_embeddings.items():
        similarity = util.pytorch_cos_sim(input_embedding, category_embedding).item()
        scores.append((code, asjc_mapping[code], similarity))

    scores.sort(key=lambda x: x[2], reverse=True)

    # Dynamically select 3 to 5 matches

    if scores[3][2] > 0.65:  # If the 4th match has a strong score, return 4 matches
        if len(scores) > 4 and scores[4][2] > 0.6:  # If 5th match is also strong, return 5
            return scores[:5]
        return scores[:4]
    return scores[:3]
     
    
def asjc_matcher_view(request):
    """Handles ASJC code matching via text input or CSV upload."""
    if request.method == "POST":
        if "text" in request.POST:
            # Single text input
            text = request.POST.get("text", "").strip()
            if not text:
                return JsonResponse({"error": "Text input is empty."}, status=400)

            results = match_asjc_codes(text)  # Assume it returns a list of (code, category, similarity)
            formatted_results = [
                {"input_text": text, "asjc_code": code, "category": category, "similarity": similarity}
                for code, category, similarity in results
            ]

            return JsonResponse({"matches": formatted_results})


        elif "file" in request.FILES:
            # Handle file upload
            file = request.FILES.get("file", None)
            if not file:
                return JsonResponse({"error": "No file uploaded."}, status=400)

            try:
                df = pd.read_csv(file)
                if "Title" not in df.columns and "Synopsis" not in df.columns:
                    return JsonResponse({"error": "CSV must contain a 'Title' or 'Synopsis' column."}, status=400)

                text_column = "Title" if "Title" in df.columns else "Synopsis"
                results = []

                for _, row in df.iterrows():
                    text = str(row[text_column])
                    matched_results = match_asjc_codes(text)
                    for code, category, similarity in matched_results:
                        results.append([text, code, category, similarity])

                # Convert results to DataFrame
                result_df = pd.DataFrame(results, columns=["Input Text", "ASJC Code", "Category", "Similarity"])
                csv_data = result_df.to_csv(index=False)

                return JsonResponse({"csv_data": csv_data, "matches": results})

            except Exception as e:
                return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=400)

    return render(request, "asjc_matcher.html")




################################END HERE######################################

#########speical character remover #################
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import re
from io import StringIO

# Define restricted characters
restricted_chars = {
    "\"": "quotation mark (U+0022)",
    "\\": "reverse solidus (U+005C)",
    "\b": "backspace (U+0008)",
    "\f": "form feed (U+000C)",
    "\n": "line feed (U+000A)",
    "\r": "carriage return (U+000D)",
    "\t": "tabulation (U+0009)"
}

# Compile regex pattern for checking restricted characters
pattern = re.compile("|".join(re.escape(char) for char in restricted_chars.keys()))

def scan_csv_for_invalid_chars(df):
    """
    Scans a DataFrame for restricted characters and returns errors.
    """
    errors = []
    for col in df.columns:
        if df[col].dtype == 'object':  # Only check string columns
            for idx, value in df[col].items():
                if isinstance(value, str):
                    match = pattern.search(value)
                    if match:
                        errors.append(
                            f"❌ Restricted character '{match.group()}' found in column '{col}' at row {idx + 1}. ({restricted_chars[match.group()]})"
                        )
    return errors

def clean_csv(df):
    """
    Removes restricted characters from string data in the DataFrame.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: pattern.sub("", x) if isinstance(x, str) else x)
    return df

def csv_validator_view(request):
    """
    Handles CSV upload, validation, correction, and download.
    """
    context = {"errors": [], "original_csv": None, "fixed_csv": None, "fixed_filename": None}

    if request.method == "POST" and request.FILES.get("csv_file"):
        uploaded_file = request.FILES["csv_file"]
        original_filename = uploaded_file.name
        fixed_filename = original_filename.replace(".csv", "_fixed.csv")

        try:
            # Read CSV into DataFrame
            csv_data = pd.read_csv(uploaded_file)

            # Scan for invalid characters
            errors = scan_csv_for_invalid_chars(csv_data)

            if errors:
                context["errors"] = errors

                # Clean CSV
                fixed_csv_data = clean_csv(csv_data.copy())

                # Convert to CSV for rendering and download
                csv_buffer = StringIO()
                fixed_csv_data.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                # Store CSV data in context for download
                context["fixed_csv"] = csv_buffer.getvalue()
                context["fixed_filename"] = fixed_filename

            context["original_csv"] = csv_data.to_html(classes="table table-bordered", index=False)

        except Exception as e:
            context["errors"].append(f"❌ Error processing CSV file: {e}")

    # Handle CSV download
    if request.method == "POST" and "download_csv" in request.POST:
        fixed_csv_data = request.POST.get("fixed_csv")
        fixed_filename = request.POST.get("fixed_filename", "fixed_file.csv")

        if fixed_csv_data:
            response = HttpResponse(fixed_csv_data, content_type="text/csv")
            response["Content-Disposition"] = f'attachment; filename="{fixed_filename}"'
            return response

    return render(request, "csv_validator.html", context)


########### end  #############################


#################scrapper using selenium Toool #######################################

import time
import pandas as pd
import csv
import io
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def extract_tr_data(html_content):
    """Extracts unique <tr> data from a page."""
    soup = BeautifulSoup(html_content, "html.parser")
    extracted_data = []
    rows = soup.find_all("tr")

    for row in rows:
        cells = tuple(cell.get_text(strip=True) for cell in row.find_all(["td", "th"]))
        if cells and cells not in extracted_data:
            extracted_data.append(cells)  # Ensure no duplicates

    return extracted_data

def extract_additional_tags(html_content):
    """Extracts specific tags like <div><p><em> and <p><time>."""
    soup = BeautifulSoup(html_content, "html.parser")
    extracted_data = []

    for tag in soup.find_all(["div", "p", "em", "time"]):
        text = tag.get_text(strip=True)
        if text and text not in extracted_data:
            extracted_data.append(text)

    return extracted_data

def handle_cookies(driver):
    """Handles cookie popups by clicking Accept/OK if found."""
    cookie_buttons = [
        "//button[contains(text(), 'Accept')]",
        "//button[contains(text(), 'I Agree')]",
        "//button[contains(text(), 'OK')]",
        "//button[contains(text(), 'Close')]",
    ]
    for xpath in cookie_buttons:
        try:
            button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            button.click()
            time.sleep(2)
            break
        except:
            continue

def get_all_read_more_links(driver):
    """Finds all 'Read More' links and returns unique hrefs."""
    read_more_links = set()
    read_more_buttons = driver.find_elements(
        By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'read')]"
    )

    for btn in read_more_buttons:
        try:
            link = btn.get_attribute("href")
            if link:
                read_more_links.add(link)  # Using set to remove duplicates
        except:
            continue

    return list(read_more_links)  # Convert back to list for indexing

def scrape_all_pages(url):
    """Extracts all 'Read More' data dynamically and returns it as a list of dictionaries."""
    
    # Initialize Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)

    handle_cookies(driver)

    scraped_data = []

    # Step 1: Collect all unique "Read More" links first
    read_more_links = get_all_read_more_links(driver)

    # Step 2: Visit each link and extract data, then return to main page
    for index, link in enumerate(read_more_links):
        try:
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            time.sleep(3)

            handle_cookies(driver)

            # Extract title
            try:
                title_element = driver.find_element(By.XPATH, "//h1|//h2|//h3")
                title_text = title_element.text.strip() if title_element.text.strip() else f"Entry {index+1}"
            except:
                title_text = f"Entry {index+1}"

            # Extract <tr> data
            page_source = driver.page_source
            tr_data = extract_tr_data(page_source)
            additional_data = extract_additional_tags(page_source)

            # Store extracted data, avoiding duplicates
            for row in tr_data:
                record = {"Title": title_text, "Row_Data": row, "Additional_Tags": " | ".join(additional_data)}
               

                if record not in scraped_data:
                    scraped_data.append(record)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"[ERROR] Skipping link {index}: {e}")

    driver.quit()
    return scraped_data

def scrapper_views(request):
    """Handles web scraping and displays results with a download option."""
    data = []

    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            data = scrape_all_pages(url)
            request.session["scraped_data"] = data  # Store data in session

    return render(request, "selenium_scrapper.html", {"data": data})

def download_csv(request):
    """Exports scraped data to CSV."""
    data = request.session.get("scraped_data", [])
    if not data:
        return HttpResponse("No data to export", content_type="text/plain")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="scraped_content.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Row_Data", "Additional_Tags"])

    for item in data:
        writer.writerow([item["Title"], ", ".join(item["Row_Data"]), item["Additional_Tags"]])

    return response


##############################################################################################


#############json validator############################
################################################


# import json
# import re
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# # Define restricted characters
# restricted_chars = {
#     "\"": "quotation mark (U+0022)",
#     "\\": "reverse solidus (U+005C)",
#     "\b": "backspace (U+0008)",
#     "\f": "form feed (U+000C)",
#     "\n": "line feed (U+000A)",
#     "\r": "carriage return (U+000D)",
#     "\t": "tabulation (U+0009)"
# }

# # Compile regex pattern for checking restricted characters
# pattern = re.compile("|".join(re.escape(char) for char in restricted_chars.keys()))

# def scan_json_for_invalid_chars(json_data, path="root"):
#     """ Recursively scans JSON data for restricted characters """
#     errors = []
#     if isinstance(json_data, dict):
#         for key, value in json_data.items():
#             errors.extend(scan_json_for_invalid_chars(key, f"{path} -> key '{key}'"))
#             errors.extend(scan_json_for_invalid_chars(value, f"{path} -> key '{key}'"))
#     elif isinstance(json_data, list):
#         for index, item in enumerate(json_data):
#             errors.extend(scan_json_for_invalid_chars(item, f"{path} -> index [{index}]"))
#     elif isinstance(json_data, str):
#         match = pattern.search(json_data)
#         if match:
#             errors.append(f"❌ Restricted character '{match.group()}' found at {path}. ({restricted_chars[match.group()]})")
#     return errors

# def clean_json(json_data):
#     """ Recursively removes restricted characters from JSON data but keeps slashes (`/`) """
#     if isinstance(json_data, dict):
#         return {key: clean_json(value) for key, value in json_data.items()}
#     elif isinstance(json_data, list):
#         return [clean_json(item) for item in json_data]
#     elif isinstance(json_data, str):
#         return pattern.sub("", json_data)  # Remove restricted characters but not `/`
#     return json_data

# @csrf_exempt
# def json_validator_view(request):
#     if request.method == "POST" and request.FILES.get("json_file"):
#         uploaded_file = request.FILES["json_file"]

#         try:
#             # Load JSON data
#             json_data = json.load(uploaded_file)
#             errors = scan_json_for_invalid_chars(json_data)

#             # If there are errors, clean the JSON
#             fixed_json_data = clean_json(json_data) if errors else json_data

#             return render(request, "json_validator.html", {
#                 "original_json": json.dumps(json_data, indent=4),
#                 "errors": errors,
#                 "fixed_json": json.dumps(fixed_json_data, indent=4) if errors else None,
#                 "filename": uploaded_file.name.replace(".json", "_fixed.json") if errors else None,
#                 "is_valid": not bool(errors),  # True if no errors, False otherwise
#             })

#         except json.JSONDecodeError as e:
#             return render(request, "json_validator.html", {"error": f"❌ Invalid JSON format: {e}"})

#     return render(request, "json_validator.html")


##################end here######################################



#view for funding body /award/opportunity
from django.shortcuts import render
# def funding_body(request):
#     return render(request, 'funding_body.html')

@login_required
def funding_body(request):
    return render(request, 'funding_body.html')
    # Replace this with your dynamic URL
    # external_url = "http://fa-macmillanlearning.highwire.org:8501/"
    # return render(request, 'funding_body.html', {'external_url': external_url})
    
    
@login_required
def opportunity(request):
    return render(request, 'opportunity.html')


@login_required
def awards(request):
    return render(request, 'awards.html')

#############QA PROCESS ######################
######QA  Page Render #############

@login_required
def qa_process(request):
    return render(request, "qa_process.html")




#QA checklist##############################
#################################

@login_required
def qa_checklist(request):
    return render(request, 'qa_checklist.html')



##########################end############################

#######url for toolbox##########
# def toolbox(request):
#       # return render(request, 'toolbox.html')
#       external_url = "http://fa-macmillanlearning.highwire.org:8502/"
     
    
#       return render(request, 'toolbox.html', {'external_url': external_url})
#updated code
@login_required
def toolbox(request):
    # External URLs
    external_url_1 = "http://fa-macmillanlearning.highwire.org:8502/"
    external_url_2 = "http://fa-macmillanlearning.highwire.org:8501/"
    external_url_3 =  "http://fa-macmillanlearning.highwire.org:8503/"

    external_url_4 =  "http://fa-macmillanlearning.highwire.org:8504/"

    # Pass these external URLs to the template
    return render(request, 'toolbox.html', {
        'external_url_1': external_url_1,
        'external_url_2': external_url_2,
        'external_url_3': external_url_3,
        'external_url_4': external_url_4,
        
    })




from django.shortcuts import render
from django.templatetags.static import static

def pdf_viewer(request):
    """Renders the UI with the embedded PDF."""
    pdf_path = static("pdfs/Funding_Body.pdf")  # Adjust the path as needed
    return render(request, 'pdf_viewer.html', {'pdf_path': pdf_path})



# MongoDB setup
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['CMS']
collection = db['Elsevier_Batch']










############code for uploading data into database############################
########################################################################


@login_required
def upload_json(request):
    if request.method == 'POST':
        uploader_name = request.POST.get('uploader_name')  # Retrieve the uploader's name
        file_type = request.POST.get('file_type')  # Retrieve the file type
        json_files = request.FILES.getlist('files')  # Get the list of uploaded files
 
        if not uploader_name or not file_type or not json_files:
            return JsonResponse({'error': 'Uploader name, file type, and files are required.'}, status=400)
 
        response_data = []
 
        try:
            for json_file in json_files:
                try:
                    # Load JSON content from the file
                    json_data = json.load(json_file)
                except json.JSONDecodeError:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'Invalid JSON format'
                    })
                    continue
 
                # Extract batchId and other IDs from JSON
                batch_id = None
                funding_body_id = None
                grant_award_id = None
                grant_opportunity_id = None
                ingestion_id = None
                unique_grant_id = None
 
                if isinstance(json_data, list) and json_data:
                    batch_id = json_data[0].get('batchId') or json_data[0].get('batch_id')
                    funding_body_id = json_data[0].get('fundingBodyId')
                    grant_award_id = json_data[0].get('grantAwardId')
                    grant_opportunity_id = json_data[0].get('grantOpportunityId')
                    ingestion_id = json_data[0].get('ingestionId')
                elif isinstance(json_data, dict):
                    batch_id = json_data.get('batchId') or json_data.get('batch_id')
                    funding_body_id = json_data.get('fundingBodyId')
                    grant_award_id = json_data.get('grantAwardId')
                    grant_opportunity_id = json_data.get('grantOpportunityId')
                    ingestion_id = json_data.get('ingestionId')
 
                # If batch_id or ingestion_id is not found, return an error
                if not batch_id:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'batchId or batch_id not found in the JSON file.'
                    })
                    continue
 
                if not ingestion_id:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'ingestionId not found in the JSON file.'
                    })
                    continue
 
                # If none of the three IDs (fundingBodyId, grantAwardId, grantOpportunityId) is found, return error
                if not (funding_body_id or grant_award_id or grant_opportunity_id):
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'At least one of the following must be present: fundingBodyId, grantAwardId, or grantOpportunityId.'
                    })
                    continue
 
                # Determine which ID to use for the unique_grant_id field (store only one)
                if funding_body_id:
                    unique_grant_id = funding_body_id
                elif grant_award_id:
                    unique_grant_id = grant_award_id
                elif grant_opportunity_id:
                    unique_grant_id = grant_opportunity_id
 
                # Check for existing record in Django ORM based on batchId
                if JSONFile.objects.filter(batch_id=batch_id).exists():
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': f'A file with batchId {batch_id} already exists in the database.'
                    })
                    continue
 
                # Save metadata using Django ORM (Ingestion ID is used as the primary key)
                JSONFile.objects.create(
                    ingestion_id=ingestion_id,  # Ingestion ID as primary key
                    uploader_name=uploader_name,
                    file_name=json_file.name,
                    file_type=file_type,
                    version=1,
                    batch_id=batch_id,  # batchId for uniqueness check
                    unique_grant_id=unique_grant_id  # Store one of the IDs: fundingBodyId, grantAwardId, or grantOpportunityId
                )
 
                # Insert JSON data into MongoDB
                if isinstance(json_data, list):
                    for item in json_data:
                        item['batchId'] = batch_id  # Ensure batchId consistency
                        item['ingestionId'] = ingestion_id  # Ensure ingestionId consistency
                        # Avoid adding uniqueGrantId to the actual JSON data
                    collection.insert_many(json_data)
                else:
                    json_data['batchId'] = batch_id
                    json_data['ingestionId'] = ingestion_id  # Ensure ingestionId consistency
                    # Avoid adding uniqueGrantId to the actual JSON data
                    collection.insert_one(json_data)
 
                # Append success response
                response_data.append({
                    'file': json_file.name,
                    'status': 'success',
                    'batchId': batch_id,
                    'uniqueGrantId': unique_grant_id
                })
 
            return JsonResponse({'message': 'Files processed', 'details': response_data})
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
 
    # Render the upload template for non-POST requests
    return render(request, 'upload.html')

############################ending uplaod json file in db ##########################################################################
###################################################################################################################################



###########################code for view data in table view that is uplaoded by user##################################################################
###########################################################################################################################################

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
from .models import JSONFile

@login_required
def getdata(request):
    try:
         
        # Fetch date filters from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter metadata based on date range
        metadata = JSONFile.objects.all()

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                metadata = metadata.filter(uploaded_at__gte=start_date_obj)
            except ValueError:
                return HttpResponse("Invalid start date format. Use YYYY-MM-DD.", status=400)

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
                metadata = metadata.filter(uploaded_at__lte=end_date_obj)
            except ValueError:
                return HttpResponse("Invalid end date format. Use YYYY-MM-DD.", status=400)
             
          
            
        
        # Start building the metadata table
        metadata_table = """
        
         
        <h1 style="background-color:#f5a142; height: 50px; color: white; text-align: center; z-index: 1000; position: fixed; width: 100%; margin: 0; top: 0; left: 0;">Metadata Table</h1>
        <div style="margin-top: 60px; padding: 10px; background-color: #f5a142; text-align: right; margin-right: 20px;">
            <form method="get" style="display: flex; align-items: center; justify-content: flex-end; gap: 15px;">
                <h4 style="margin: 0; color: white;">Search Data</h4>
                <div>
                    <label for="start_date" style="margin-right: 5px; color: white;">Start Date:</label>
                    <input type="date" id="start_date" name="start_date" value="{start_date or ''}" class="filter-input">
                </div>
                <div>
                    <label for="end_date" style="margin-right: 5px; color: white;">End Date:</label>
                    <input type="date" id="end_date" name="end_date" value="{end_date or ''}" class="filter-input">
                </div>
                <button type="submit" class="filter-btn">Filter</button>
            </form>
        </div>
        <table border="1" style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr>
                    <th>Sr. No</th>
                    <th>MPS Id</th>
                    <th>Uploader Name</th>
                    <th>File Name</th>
                    <th>File Type</th>
                    <th>Version</th>
                    <th>Uploaded At</th>
                    <th>Unique Grant ID</th>
                    <th>Ingestion ID</th>
                    <th>View File</th>
                    <th>Download File</th>
                </tr>
            </thead>
            <tbody>
        """

        for idx, file in enumerate(metadata, start=1):
            batch_id = file.batch_id
            uploader_name = file.uploader_name
            file_type = file.file_type
            unique_grant_id = file.unique_grant_id
            ingestion_id = file.ingestion_id
            view_url = reverse('view_json', args=[batch_id])
            download_url = reverse('download_json', args=[batch_id])

            metadata_table += f"""
            <tr>
                <td>{idx}</td>
                <td>{batch_id}</td>
                <td>{uploader_name}</td>
                <td>{file.file_name}</td>
                <td>{file_type}</td>
                <td>{file.version}</td>
                <td>{file.uploaded_at}</td>
                <td>{unique_grant_id}</td>
                <td>{ingestion_id}</td>
                <td>
                    <a href="{view_url}" style="text-decoration: none; color: blue;">View</a>
                </td>
                <td>
                    <a href="{download_url}" style="text-decoration: none; color: green;">Download</a>
                </td>
            </tr>
            """
        metadata_table += "</tbody></table>"

        # Combine and return the complete HTML response
        html_response = f"""
        <html>
        <head>
            <title>Data Table</title>
            <style>
                table {{ border: 1px solid black; border-collapse: collapse; width: 100%; background-color: #ffffff; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid black; background-color: #ffffff; border: 1px solid #ddd; }}
                th {{ background-color:#f5a142; color: white; }}

                .filter-input, .filter-btn {{
                    padding: 8px 15px;
                    border-radius: 5px;
                    border: 1px solid #f5a142;
                    font-size: 14px;
                }}

                .filter-input {{
                    background-color: white;
                    color: #333;
                    transition: background-color 0.3s ease;
                }}

                .filter-input:hover {{
                    background-color: #f5a142;
                    color: white;
                }}

                .filter-btn {{
                    background-color: #f5a142;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }}

                .filter-btn:hover {{
                    background-color: #e58a3d;
                }}
            </style>
        </head>
        <body>
           
            {metadata_table}
        </body>
        </html>
        """
        return HttpResponse(html_response)

    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


###################adding feild descriptions####################################33
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient

# Static descriptions for key fields
FIELD_DESCRIPTIONS = {
    "batchId": "Its Internal Id Created at ingestion time",
    "ingestionId": "When File Ingested it Created at ingestion time",
    "grantAwardId": "Assigned by suppliers as the unique Elsevier identifier for the award",
    "fundingBodyAwardId": "Contains the unique identifier given to the award by the Funding Body. If not available, use 'Not available'.",
    "hasInstallment":"HasInstallment",
    "hasWorkPackage":"hasWorkPackage",
    "homePage":"URL of the funding body homepage where the award is capturing",
    "link":"URL pointing to a project page or to the funder page with further details about the funded project",
    "synopsis":" contains a description of the funding opportunity identifying the exact goal of the opportunity focusing on the research objectives. FBs use different names for synopses, such as Research objectives, Description, Purpose, Abstract, and Summary.",
    "abstract":"Abstract",
    "title":"Title",
    "language":"Language Type",
    "value":"Value",
    "hasProvenance":"All standard details for the opportunity records, such as the supplier details, status of the record, and the creation and update details can be found in the object Provenance",
    "createdOn":"Creation Date",
    "createdBy":"Created By",
    "createdWith":"Created With",
    "source":"Source",
    "licenseInformation":" FBs require that Elsevier cite the FB license when using their data in a commercial product. Use property licenseInformation to capture information attributing the data to the FB. Capture all data in the available fields.",
    "funds":"The property funds contains the object AwardFund with the sub-properties such as fundingProjectId,acronym,hasPart,title,startDate,endDate,hasPostalAddress,link,status",
    "fundingBodyProjectId":"ID of the project that is funded as defined by the funding organization.",
    "hasPart":"Used if some of the funding is derived from a subproject as mentioned by the FB.",
    "budget":" budget is used to indicate the total (sub)project cost whether funded or not and contains the object AmountWithCurrency",
    "currency":"currency contains a value indicating the award currency. If the currency type is not specified, use the currency for the country of the FB awarding the opportunity or award.",
    "amount":"amount is captured in positive integers only. If not indicated in the source, do not capture this object. ",
    "acronym":"Acronym of the project this award is funding",
    "hasPostalAddress":"Location where the award or project took place, contains the object PostalAddress",
    "addressCountry":"Capture the 3-letter codes in lowercase from Country Codes for OPSBANK (2 and 3 letters).",
    "addressRegion":"The administrative region, state or area used, for states or provinces in the USA, Canada,and Australia, use letter codes in uppercase in USA, Canada and Australia Province/State Abbreviations.",
    "addressLocality":"The locality such as the settlement name, city, town, or county (a territorial division of some countries)",
    "addressPostalCode":"A series of letters, digits, or both that specifies a geographic location included in a postal address. Basic US postal or ZIP codes contain 5 digits. ZIP codes may also be given as the IP+4 code in which the basic 5-digit code is extended with 4 extra digits, separated from the basic code with a hyphen, capture as written in the source.",
    "postOfficeBoxNumber":"A uniquely addressable lockable box located on the premises of a post office station included in a postal address.",
    "streetAddress":"The location of a building, apartment, or other structure on a street, including the house number, if available",
    "status":"status is used to indicate whether an FB is active or inactive. 'ACTIVE' indicates whether the funder is currently providing funding. 'INACTIVE' indicates a past funder that is no longer providing funding or no longer exists.The default value is 'ACTIVE'",
    "fundingDetail":"contains the funding details of the awards",
     "installment":"contains the information representing the awardedm amount for each installment or fiscal year.",
    "index":"index indicates the number of installments, with each new installment adding to the index. Default is 1.",
    "grantAwardInstallmentId":"GrantAwardInstallmentId",
    "financialYearStart":"FinancialYearStart",
    "financialYearEnd":"FinancialYearEnd",
    "fundedAmount":" fundedAmount contains the amount that was awarded in the installment.",
    "fundingTotal":"contains the digits representing the total funding assigned to a project through this award, if there are installments this number represents the sum of all yearly installments",
    "awardeeDetail":"contains information about these award recipients. If there are multiple awardees, capture each in a new set of sub-properties in awardeeDetail.",
    "activityType":"is an open text field used to indicate the type of organization activity as found in the award announcement, that is, research organization or industry.",
    "affiliationOf":"Awardees within the institution who received the award or will work on the funded project are captured in the property affiliationOf.",
    "awardeePersonId":" is a generated identifier for each instance of an awarded person or researcher. The supplier creates the awardeePersonId value by capturing the grantAwardId value, followed by _P_(sequence number),",
    "emailAddress":"Capture the email address of the awardee in the property emailAddress when available in the source.",
    "familyName:":"Capture the surname of the awardee, in most cases this is the last name.",
    "fundingBodyPersonId":"FundingBodyPersonId: ",
    "givenName":"Capture the first name of the awardee",
    "identifier":"The property identifier is a container property for referencing other organizational identifiers.",
    "type":"Type Of",
    "initials":"Capture the initials of the given name of an awardee in the property initials. Capture initials in uppercase and with a period. Hyphenated given names must include the hyphen. If more than one initial appears, capture the initials without spaces between them.",
    "name":"Name Capture the full name as it appears in the source in the property name using the object StringWithLanguage, ",
    "role":"role is used to indicate the role of the awarded institution in the project if provided by the FB. The default valueis 'COORDINATOR'. This information is normally provided for EU data.",
    "sourceRole":"sourceRole",
    "awardeeAffiliationId":"AwardeeAffiliationId:",
    "departmentName":"Any affiliation department mentioned in the announcement is captured in the property departmentName using object StringWithLanguage",
    "fundingBodyOrganizationId":"FundingBodyOrganizationId",
    "vatNumber":"The funder-specific VAT number is captured in the property vatNumber when found in the source.",
    "classification":"Classification contains classification types and codes for an opportunity or award. Classifications refers to the vocabularies that are applied to opportunities or awards in order to classify or categorize these records on their type,research area, funding mechanism, or focus area",
    "hasSubject":"In sub-property preferredLabel, capture the term of the classification code. In the sub-property identifier, capture the corresponding value and the type of classification",
    "preferredLabel":"capture the term of the classification code",
     "relatedOpportunity":" describes the relationship between an opportunity and any awards made from that opportunity. If described, capture this information",
     "grantOpportunityId":" grantOpportunityId is created and assigned by suppliers as the unique Elsevier identifier for the opportunity",
     "fundingBodyOpportunity":"fundingBodyOpportunityId is used to capture the unique identifier number given to the opportunity by the FB. If the FB does not publish an ID, a number, code, or other identifier for the opportunity, use the value 'Not available' in the property fundingBodyOpportunityId",
    "relatedFunder":"relatedFunder, capture FBs that have financed the award that resulted in this publication,such as  leadFunder and hasFunder",
    "leadFunder":"main funder of the award. If a funder has a complex hierarchy, take the lowest level of the hierarchy. If multiple funders are mentioned, capture the one which is reporting the award-to-publication link",
     "fundingBodyId":" fundingBodyId contains the unique identifier for the created FB, using the range of IDs provided by Elsevier",
     "sourceId":"SourceId",
     "sourceText":"SourceText",
     "hasProvenance":"All standard details for the award records, such as the supplier details, status of the record, and the creation and update details are captured in hasProvenance",
     "wasAttributedTo":"Identifier of the data provider for the record: SUP001, SUP002, SUP003, or NOTSPECIFIED",
     "derivedFrom":"Source URL of the record",
     "createdOn":"Date that the record was created (as per supplier CMS)",
     "lastUpdateOn":"Date when the record was updated (as per supplier CMS)",
     "contactPoint":"Contact email address of the supplier that can be used to address any issues regarding the record",
     "version":"Record version number, increased for each update ",
     "hidden":"Boolean; 'true' indicating that the record will not be displayed on customer-facing products",
     "defunct":"Boolean; 'true' indicating that the record has been tagged as invalid, such as a duplicate, and is no longer used by Elsevier products",
     "status":"Status of the record: 'NEW', 'UPDATE', or 'DELETE'",
     "options":"options",
     "additionalProp1":" AdditionalProp1",
     "additionalProp2":" AdditionalProp2",
     "additionalProp3":"AdditionalProp3",
     "hasFunder":" contains all funders listed as contributing to the award that funds the publication. The list must also contain the lead funder, and any other listed funders.",
    "description":"Description",
    "keyword":" Keywords normally reflect the main research topics that the funding opportunity covers. FB can also refer to tags, topics, categories, areas, and subjects.",
    "grantType": "contains only the opportunity type that is distributed by the funder in a structured manner. The default category is the value 'RESEARCH'",
    "funderSchemeType":" is used to indicate the type of funding provided by the funder for this opportunity as stated in the opportunity announcement. Supplier captures the original funder text or description that is used to determine the set,specific categories used in grantType.",
    "startDate":"The date from which applications for an opportunity will be accepted.",
}

def json_to_html_form(data, level=0, parent_id="root"):
    """
    Recursive function to generate an expandable/collapsible HTML form representation of JSON data.
    Adds hover descriptions for specific fields.
    """
    html = ""
    current_id = f"{parent_id}_{level}"

    if isinstance(data, dict):
        for key, value in data.items():
            item_id = f"{current_id}_{key}"
            description = FIELD_DESCRIPTIONS.get(key, "No description available")  # Default description

            if isinstance(value, (dict, list)):
                # Expandable section for nested fields
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <span style="cursor: pointer; color: blue;" onclick="toggle('{item_id}')" title="{description}">
                        ▶ <b>{key}</b>
                    </span>
                    <div id="{item_id}" style="display: none; margin-top: 5px;">
                        {json_to_html_form(value, level + 1, item_id)}
                    </div>
                </div>
                """
            else:
                # Highlight missing or 'not found' data
                highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if value in [None, "", "not found", "not available", "NOT FOUND"] else ""
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <label style="font-weight: bold;" for="{item_id}" title="{description}">{key}:</label>
                    <input type="text" id="{item_id}" value="{value}" 
                           style="margin-left: 10px; padding: 7px; width:400px; {highlight_style}" readonly/>
                </div>
                """

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            item_id = f"{current_id}_item_{idx}"
            if isinstance(item, (dict, list)):
                # Expandable section for list items
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <span style="cursor: pointer; color: green;" onclick="toggle('{item_id}')">
                        ▶ <b>Item {idx + 1}</b>
                    </span>
                    <div id="{item_id}" style="display: none; margin-top: 5px;">
                        {json_to_html_form(item, level + 1, item_id)}
                    </div>
                </div>
                """
            else:
                # Highlight missing or 'not found' data
                highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if item in [None, "", "not found", "not available", "NOT FOUND"] else ""
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <label style="font-weight: bold;">Item {idx + 1}:</label>
                    <input type="text" value="{item}" style="margin-left: 10px; padding: 3px; {highlight_style}" readonly/>
                </div>
                """

    return html


def view_json(request, batch_id):
    """
    View function to fetch JSON data from MongoDB and render it as an expandable HTML form view.
    Also logs available batch IDs for debugging.
    """
    try:
        
        # Debug: Print available batch IDs
        available_batch_ids = collection.distinct("batchId")
        print("Available batch_ids in MongoDB:", available_batch_ids)

        # Query to fetch the data
        query = {
            '$or': [
                {'batch_id': batch_id},
                {'batchId': batch_id},
                {'BatchId': batch_id},
                {'batchid': batch_id}
            ]
        }
        json_data = collection.find_one(query, {'_id': 0})

        if not json_data:
            return HttpResponse(
                f"<h1 style='color: red;'>No data found for batch_id: {batch_id}</h1>", status=404
            )

        # Generate HTML with expandable/collapsible functionality
        html_content = f"""
        <html>
        <head>
            <title>JSON Data View</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f7f7f7;
                }}
                h1 {{
                    text-align: center;
                    background-color:#f5a142;
                    color: white;
                    padding: 10px;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 10px;
                    border: 1px solid #ddd;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                input {{
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 3px 5px;
                }}
                label {{
                    font-weight: bold;
                    display: inline-block;
                    width: 150px;
                }}
            </style>
            <script>
                function toggle(id) {{
                    var element = document.getElementById(id);
                    var span = event.target;

                    if (element.style.display === "none") {{
                        element.style.display = "block";
                        span.innerHTML = "▼ " + span.innerHTML.slice(2);
                    }} else {{
                        element.style.display = "none";
                        span.innerHTML = "▶ " + span.innerHTML.slice(2);
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>JSON Data for Batch ID: {batch_id}</h1>
            <div class="container">
                {json_to_html_form(json_data)}
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content)

    except Exception as e:
        print("Error occurred:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

####################end#################





############downlaod function to upload a file ####################
############################################
import json
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient


def download_json(request, batch_id):
    """
    View function to fetch JSON data from MongoDB and allow the user to download it as a .json file.
    """
    try:
        # Fetch JSON data based on batch_id (flexible query)
        query = {
            "$or": [
                {"batch_id": batch_id},
                {"batchId": batch_id},
                {"BatchId": batch_id}
            ]
        }
        json_data = collection.find_one(query, {"_id": 0})  # Exclude the MongoDB '_id' field

        if not json_data:
            # Return 404 response if no data is found
            return JsonResponse(
                {"error": f"No data found for batch_id: {batch_id}"},
                status=404
            )

        # Create the HTTP response with JSON content type
        response = HttpResponse(
            json.dumps(json_data, indent=4),  # Indented JSON for readability
            content_type="application/json"
        )
        # Set the 'Content-Disposition' header to force download
        response["Content-Disposition"] = f'attachment; filename="{batch_id}.json"'

        return response

    except Exception as e:
        print("Error while processing JSON file download:", str(e))
        return JsonResponse(
            {"error": "An internal error occurred while processing the request."},
            status=500
        )
#######################################################
########################################################################################
  
    
    
    
    
  # Update JSON File
def update_json(request):
    if request.method == 'POST':
        batch_id = request.POST['batch_id']
        json_file = request.FILES['file']

        try:
            # Read JSON content
            json_data = json.load(json_file)

            # Update metadata version
            file_metadata = JSONFile.objects.get(batch_id=batch_id)
            file_metadata.version += 1
            file_metadata.save()

            # Update MongoDB data (replace existing records for the batch)
            collection.delete_many({'batch_id': batch_id})
            if isinstance(json_data, list):
                for item in json_data:
                    item['batch_id'] = batch_id
                collection.insert_many(json_data)
            else:
                json_data['batch_id'] = batch_id
                collection.insert_one(json_data)

            return JsonResponse({'message': 'File updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        
        
        
        
# #############adding view for source input data form #########################################
#############################################################################################
# # import datetime
# from datetime import datetime
# from django.shortcuts import render, redirect
# from .forms import SourceMetadataForm
# from .models import SourceMetadata  # Import the MongoDB model
# # MongoDB setup



# def upload_source_metadata(request):
#     if request.method == 'POST':
#         form = SourceMetadataForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save form data to MongoDB
#             source_metadata = SourceMetadata(
#                 import_url=form.cleaned_data['import_url'],
#                 date_of_arrival=form.cleaned_data['date_of_arrival'],
#                 assigned_to=form.cleaned_data['assigned_to'],
#                 frequency_of_site_updates=form.cleaned_data['frequency_of_site_updates'],
#                 site_last_checked=form.cleaned_data['site_last_checked'],
#                 source_file_upload=form.cleaned_data.get('source_file_upload'),
#                 json_file_name=form.cleaned_data['json_file_name'],
#                 json_upload_date=form.cleaned_data['json_upload_date'],
#                 sup_id=form.cleaned_data['sup_id'],
#                 sme_comments=form.cleaned_data['sme_comments'],
#                 screenshots_taken=form.cleaned_data['screenshots_taken'],
                
                
#                  # New fields for QA
#                 qa_comment=form.cleaned_data.get('qa_comment'),
#                 qa_name=form.cleaned_data.get('qa_name'),
#                 qa_issue=form.cleaned_data.get('qa_issue'),
#                 # created_at=datetime.datetime.now() , 
#                 created_at = datetime.now()
#             )
#             source_metadata.save()  # Save the document into MongoDB
#             return redirect('/')  # Redirect after success
#     else:
#         form = SourceMetadataForm()

#     return render(request, 'upload_source_metadata.html', {'form': form})

# #########################################################
# ##########ending input source data##########################




# #######################function for viewing source inp[ut data into table view#########################################################

# def view_source_metadata(request):
#     # Fetch all source metadata records from MongoDB
#     source_metadata_list = SourceMetadata.objects.all()

#     return render(request, 'view_source_metadata.html', {'source_metadata_list': source_metadata_list})


#updated code for source metadata correct code
#date 13-1-2025


from django.shortcuts import render, redirect, get_object_or_404
from .forms import SourceMetadataForm
from .models import SourceMetadata
from django.http import Http404
from datetime import datetime
import os
from django.conf import settings
#Upload view
@login_required
def upload_source_metadata(request):
    if request.method == 'POST':
        form = SourceMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('source_file_upload')
            if uploaded_file:
                # Define the file path where the file will be saved
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'source_files')
                os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
                file_path = os.path.join(upload_dir, uploaded_file.name)

                # Save the file to the local file system
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            # Save form data to MongoDB
            source_metadata = SourceMetadata(
                import_url=form.cleaned_data['import_url'],
                date_of_arrival=form.cleaned_data['date_of_arrival'],
                assigned_to=form.cleaned_data['assigned_to'],
                frequency_of_site_updates=form.cleaned_data['frequency_of_site_updates'],
                site_last_checked=form.cleaned_data['site_last_checked'],
                source_file_upload=uploaded_file.name if uploaded_file else None,
                json_file_name=form.cleaned_data['json_file_name'],
                json_upload_date=form.cleaned_data['json_upload_date'],
                sup_id=form.cleaned_data['sup_id'],
                sme_comments=form.cleaned_data['sme_comments'],
                screenshots_taken=form.cleaned_data['screenshots_taken'],
                
                # New fields for QA
                qa_comment=form.cleaned_data.get('qa_comment'),
                qa_name=form.cleaned_data.get('qa_name'),
                file_status =form.cleaned_data.get('file_status'),
                qa_issue=form.cleaned_data.get('qa_issue'),
                created_at=datetime.now()
            )
            source_metadata.save()  # Save the document into MongoDB
            # return redirect('/')  # Redirect after success
            return redirect('/funding_body/')

            
    else:
        form = SourceMetadataForm()

    return render(request, 'upload_source_metadata.html', {'form': form})




 ############################## View source metadata#####################################
@login_required
def view_source_metadata(request):
    # Fetch all source metadata records from MongoDB
    source_metadata_list = SourceMetadata.objects.all()
    for i in source_metadata_list:
        print(i)

    return render(request, 'view_source_metadata.html', {'source_metadata_list': source_metadata_list})




###############################code for edit sourcemetadata############################

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from .forms import SourceMetadataForm
from .models import SourceMetadata
from datetime import datetime
from django.http import HttpResponseBadRequest

from bson import ObjectId
def edit_source_metadata(request, metadata_id):
    #print(f"Received metadata_id: {metadata_id}")  #Debugging

    if not metadata_id or metadata_id == "None":
        return HttpResponseBadRequest("Invalid metadata ID")
    try:
        # Try fetching the object from the MongoDB database
        object_id = ObjectId(metadata_id) 
        source_metadata = SourceMetadata.objects.get(id=object_id)
    except SourceMetadata.DoesNotExist:
        raise Http404("SourceMetadata not found")

    # Restrict access: Only the assigned user, QA user, or a superuser can edit
    if (request.user.username != source_metadata.assigned_to and 
        request.user.username != source_metadata.qa_name and 
        not request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed to edit this entry.")

    if request.method == 'POST':
        form = SourceMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('source_file_upload') 
            if uploaded_file:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'source_files')
                os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                source_metadata.source_file_upload = uploaded_file.name
            # Update the metadata object
            source_metadata.import_url = form.cleaned_data['import_url']
            source_metadata.date_of_arrival = form.cleaned_data['date_of_arrival']
            source_metadata.assigned_to = form.cleaned_data['assigned_to']
            source_metadata.frequency_of_site_updates = form.cleaned_data['frequency_of_site_updates']
            source_metadata.site_last_checked = form.cleaned_data['site_last_checked']
            #source_metadata.source_file_upload = uploaded_file.name if uploaded_file else None,
            source_metadata.json_file_name = form.cleaned_data['json_file_name']
            source_metadata.json_upload_date = form.cleaned_data['json_upload_date']
            source_metadata.sup_id = form.cleaned_data['sup_id']
            source_metadata.sme_comments = form.cleaned_data['sme_comments']
            source_metadata.screenshots_taken = form.cleaned_data['screenshots_taken']
            
            # QA fields
            source_metadata.qa_comment = form.cleaned_data.get('qa_comment')
            source_metadata.qa_name = form.cleaned_data.get('qa_name')
            source_metadata.file_status= form.cleaned_data.get('file_status')
            source_metadata.qa_issue = form.cleaned_data.get('qa_issue')
            
            source_metadata.save()  # Save changes to the database
            return redirect('view_source_metadata')  # Redirect to the list view after saving
    else:
        # Pre-fill the form with existing metadata
        initial_data = {
            'import_url': source_metadata.import_url,
            'date_of_arrival': source_metadata.date_of_arrival,
            'assigned_to': source_metadata.assigned_to,
            'frequency_of_site_updates': source_metadata.frequency_of_site_updates,
            'site_last_checked': source_metadata.site_last_checked,
            'source_file_upload': source_metadata.source_file_upload,
            'json_file_name': source_metadata.json_file_name,
            'json_upload_date': source_metadata.json_upload_date,
            'sup_id': source_metadata.sup_id,
            'sme_comments': source_metadata.sme_comments,
            'screenshots_taken': source_metadata.screenshots_taken,
            'qa_comment': source_metadata.qa_comment,
            'qa_name': source_metadata.qa_name,
            'file_status': source_metadata.file_status,
            'qa_issue': source_metadata.qa_issue,
        }
        form = SourceMetadataForm(initial=initial_data)

    return render(request, 'upload_source_metadata.html', {'form': form, 'metadata': source_metadata})



   #######################function for viewing source input data into table view#########################################################     
        

        
        
        

# def manage_files(request):
#     """
#     View to display all files and handle updates through inline editing.
#     """
#     if request.method == 'POST' and 'save_updates' in request.POST:
#         batch_id = request.POST['batch_id']
#         updated_data = request.POST['updated_data']  # Data from the form (as JSON string)

#         try:
#             # Fetch the original file metadata
#             file_metadata = get_object_or_404(JSONFile, batch_id=batch_id)

#             # Parse the updated data
#             updated_json = json.loads(updated_data)

#             # Increment version and save metadata
#             new_version = file_metadata.version + 1
#             file_metadata.version = new_version
#             file_metadata.save()

#             # Update MongoDB collection
#             collection.delete_many({'batch_id': batch_id})
#             if isinstance(updated_json, list):
#                 for item in updated_json:
#                     item['batch_id'] = batch_id
#                 collection.insert_many(updated_json)
#             else:
#                 updated_json['batch_id'] = batch_id
#                 collection.insert_one(updated_json)

#             # Save update to the history table
#             JSONFileUpdateHistory.objects.create(
#                 json_file=file_metadata,
#                 batch_id=batch_id,
#                 version=new_version,
#                 update_details=updated_json
#             )

#             return JsonResponse({'message': 'File updated successfully!'})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # Fetch all files for the table
#     files = JSONFile.objects.all()
#     return render(request, 'manage_files.html', {'files': files})


# def updated_files(request):
#     """
#     View to display the update history table.
#     """
#     updates = JSONFileUpdateHistory.objects.all()
#     return render(request, 'updated_files.html', {'updates': updates})


#code for viewing only funding /award/opportunity data
# View for Funding Body
@login_required
def funding_body_view(request):
    if request.method == 'GET':
        # Extract funding_body_id from GET parameters
        funding_body_id = request.GET.get('funding_body_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for funding body data
        filters = {'file_type__iexact': 'FundingBody'}  # Updated value
        
        # Add unique_grant_id filter if provided
        if funding_body_id:
            filters['unique_grant_id'] = funding_body_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No funding body data found.")  # Debugging
            return JsonResponse({'message': 'No funding body data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'funding_body_view.html', {'files': response_data})

#award data view function################################################################
@login_required
def award_view(request):
    if request.method == 'GET':
        # Extract award_id from GET parameters
        award_id = request.GET.get('award_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for award data
        filters = {'file_type__iexact': 'Award'}  # Assuming 'Award' is the value for file_type
        
        # Add unique_grant_id filter if provided
        if award_id:
            filters['unique_grant_id'] = award_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Award Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No award data found.")  # Debugging
            return JsonResponse({'message': 'No award data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'award_view.html', {'files': response_data})

@login_required
def opportunity_view(request):
    if request.method == 'GET':
        # Extract opportunity_id from GET parameters
        opportunity_id = request.GET.get('opportunity_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for opportunity data
        filters = {'file_type__iexact': 'Opportunity'}  # Assuming 'Opportunity' is the value for file_type
        
        # Add unique_grant_id filter if provided
        if opportunity_id:
            filters['unique_grant_id'] = opportunity_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Opportunity Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No opportunity data found.")  # Debugging
            return JsonResponse({'message': 'No opportunity data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'opportunity_view.html', {'files': response_data})





#file ingestion view function for json ############################
###################################################################



# 17:40
#view code for ingestion main page#############################3

def ingestion_main_temp(request):
    return render(request, 'ingestion_main.html')  # Page with Tabs


#################view code of ingestion of files for uat  ###########################
################################################################################################
##############################################################################################

from django import forms
import os
import base64
import logging
import requests
from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .forms import FileIngestionForm
from .models import IngestionLog

# Create logs directory in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "ingestion_details.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global token variable
global_token = None


def oauth_token(key, secret):
    url = "https://uat.business.api.elsevier.com/token"
    credentials = f"{key}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

from django.core.files.base import ContentFile
@csrf_exempt
@login_required

def file_ingestion(request):
    # global global_token
    context = {"form": FileIngestionForm()}
    global_token = request.session.get("oauth_token")

    if request.method == "POST":
        form = FileIngestionForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.cleaned_data["action"]
            # Ensure `user_name` defaults to "Unknown User" if not provided
            user_name = form.cleaned_data.get("user_name", "Unknown User")

            # Debugging log to verify if user_name is correctly passed from the form
            logging.info(f"Form submitted by user: {user_name}")

            if action == "generate_token":
                key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
                secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
                global_token = oauth_token(key, secret)
                #context["token"] = global_token
                #context["message"] = (
                #    "Token generated successfully!" if global_token else "Failed to generate token."
                #)
                #log_message = f"User: {user_name} - Token generation status: {'Success' if global_token else 'Failure'}"
                #logging.info(log_message)
                if global_token:
                    request.session["oauth_token"] = global_token  # Store token in session
                    request.session.set_expiry(3600)  # Optional: Set expiry to 1 hour (adjust as needed)
                    context["token"] = global_token
                    context["message"] = "Token generated successfully!"
                    logging.info(f"User: {user_name} - Token generated successfully!")
                else:
                    context["message"] = "Failed to generate token."
                    logging.warning(f"User: {user_name} - Token generation failed.")

            elif action == "create_batch":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestion_template.html", context)

                uploaded_file = request.FILES.get("file_location")
                if not uploaded_file:
                    context["message"] = "No file uploaded."
                    return render(request, "ingestion_template.html", context)

                headers = {
                    "Authorization": f"Bearer {global_token}",
                    "accept": "*/*",

                }
                if not os.path.exists(default_storage.location):
                    os.makedirs(default_storage.location, exist_ok=True)

                #temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
                #if not os.path.exists(default_storage.location):
                #    os.makedirs(default_storage.location)

                #with default_storage.open(temp_file_path, 'wb+') as temp_file:
                #    for chunk in uploaded_file.chunks():
                #        temp_file.write(chunk)
                try:
                    file_path = os.path.join("uploads", uploaded_file.name)
                    file_name = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                    full_file_path = default_storage.path(file_name)  # Get full path
                    logging.info(f"File saved at: {full_file_path}")


                    with open(full_file_path, 'rb') as file:
                        files = {'file': file}
                        response = requests.post(
                            "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
                            headers=headers,
                            files=files,
                        )

                    if response.status_code == 200:
                        batch_id = response.json().get("batchId")
                        if batch_id:
                            context["batch_id"] = batch_id
                            context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
                            logging.info(f"User: {user_name} - Batch ID: {batch_id}")
                        else:
                            context["message"] = "Batch creation successful but no batch ID returned."
                            logging.warning(f"User: {user_name} - Batch created, but no batch ID.")
                    else:
                        context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
                        logging.error(f"User: {user_name} - Batch creation failed. Response: {response.text}")

                except PermissionError as e:
                    context["message"] = "Permission denied while saving the file."
                    logging.error(f"User: {user_name} - PermissionError: {e}")

                except Exception as e:
                    context["message"] = "An error occurred while saving the file."
                    logging.exception(f"User: {user_name} - Exception: {e}")
                #with open(temp_file_path, 'rb') as file:
                #    files = {'file': file}
                #    response = requests.post(
                #        "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
                #        headers=headers,
                #        files=files,
                        
                #    )
                   

                #if response.status_code == 200:
                #    batch_id = response.json().get("batchId")
                #    if batch_id:
                #        context["batch_id"] = batch_id
                #        context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
                #        log_message = f"User: {user_name} - Batch created successfully! Batch ID: {batch_id}"
                ##        logging.info(log_message)
                 #   else:
                 #       context["message"] = "Batch creation successful but no batch ID returned."
                 #       logging.warning(f"User: {user_name} - Batch creation successful but no batch ID returned.")
                #else:
                #    context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
                #    logging.error(f"User: {user_name} - Failed to create batch. Response Code: {response.status_code}")

            elif action == "ingest_file":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestion_template.html", context)

                ingestion_type = form.cleaned_data["ingestion_type"]
                batch_id = request.POST.get("batch_id")
                file = request.FILES.get("json_location")
                data_type = form.cleaned_data["data_type"]

                if not file:
                    context["message"] = "No file provided for ingestion."
                    return render(request, "ingestion_template.html", context)

                base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
                url = f"{base_url}/{data_type}"
                if ingestion_type == "batch":
                    url += "/bulk"

                headers = {
                    "accept": "application/json",
                    "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
                    "Content-Type": "application/json",
                    "batchId": batch_id,
                    "Authorization": f"Bearer {global_token}",
                }

                try:
                    response = requests.post(url, headers=headers, data=file.read())
                    ingestion_response = response.json()

                    ingestion_id = ingestion_response.get("ingestionId")
                    ingestion_item_id = ingestion_response.get("id")

                    if ingestion_id and ingestion_item_id:
                        log_message = (
                            f"User: {user_name} - Timestamp: {datetime.now()} - "
                            f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
                        )
                        logging.info(log_message)
                        
                        # Store details in the database
                        store_ingestion_details(user_name, ingestion_id, ingestion_item_id, batch_id)

                    if response.status_code == 200:
                        context["message"] = "File ingested successfully!"
                    else:
                        context["message"] = f"Failed to ingest file: {response.text}"
                        logging.error(f"User: {user_name} - Failed to ingest file: {response.text}")

                except Exception as e:
                    context["message"] = "An error occurred during file ingestion."
                    logging.exception(f"User: {user_name} - Exception occurred during file ingestion: {e}")
                    
 # Step 5: Check Ingestion Status
            elif action == "check_ingestion_status":
                ingestion_id = request.POST.get("ingestion_id")
                data_type = request.POST.get("data_type")

                if not ingestion_id:
                    context["ingestion_status_message"] = "Please provide an ingestion ID."
                    return render(request, "ingestion_template.html", context)

                base_urls = {
                    "award": "https://uat.business.api.elsevier.com/v1/funding-ingestion/award/",
                    "opportunity": "https://uat.business.api.elsevier.com/v1/funding-ingestion/opportunity/",
                    "funding-body": "https://uat.business.api.elsevier.com/v1/funding-ingestion/funding-body/"
                }

                url = f"{base_urls[data_type]}{ingestion_id}"
                headers = {"accept": "application/json", "Authorization": f"Bearer {global_token}"}

                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        response_data = response.json()
                        context["ingestion_status_message"] = f"Status: {response_data.get('status', 'Unknown')}"
                    else:
                        context["ingestion_status_message"] = f"Failed to fetch status. Response Code: {response.status_code}"
                except Exception as e:
                    context["ingestion_status_message"] = "An error occurred while checking ingestion status."
                    logging.exception(f"User: {user_name} - Exception during status check: {e}")
                    context["ingestion_status_message"] = "Failed to fetch status."

    return render(request, "ingestion_template.html", context)
    



################view code for storing imgestion details in db  ##########


def store_ingestion_details(user_name, ingestion_id, ingestion_item_id, batch_id):
    """Store ingestion details in the database."""
    IngestionLog.objects.create(
        user_name=user_name,
        ingestion_id=ingestion_id,
        ingestion_item_id=ingestion_item_id,
        batch_id=batch_id,
        status="Success"  # Initially set status as Success, update if needed
    )

####################code for displaying ingestion details in table view in ui##################################
from django.shortcuts import render
from .models import IngestionLog

@login_required
def ingestion_logs_view(request):
    # Fetch all ingestion logs from the database
    ingestion_logs = IngestionLog.objects.all()

    context = {
        'ingestion_logs': ingestion_logs
    }
    return render(request, 'ingestion_logs.html', context)




#############################end#########################################
#################view code of ingestion of files for prod ###########################
################################################################################################

from django import forms
import os
import base64
import logging
import requests
from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .forms import IngestionProd
from .models import IngestProd

# Create logs directory in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "ingest_logs.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global token variable
global_token = None


def get_oauth_token(key, secret):
    url = "https://business.api.elsevier.com/token"
    credentials = f"{key}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


from django.core.files.base import ContentFile
@csrf_exempt
@login_required

def ingestion_prod(request):
    #global global_token
    context = {"form": IngestionProd()}
    global_token = request.session.get("get_oauth_token")

    if request.method == "POST":
        form = IngestionProd(request.POST, request.FILES)

        if form.is_valid():
            action = form.cleaned_data["action"]
            # Ensure `user_name` defaults to "Unknown User" if not provided
            user_name = form.cleaned_data.get("user_name", "Unknown User")

            # Debugging log to verify if user_name is correctly passed from the form
            logging.info(f"Form submitted by user: {user_name}")

            if action == "generate_token":
                key = "P2jBnk8mUNIHqBHNE4SXs4QhklMdB25F"  # Replace with your actual key
                secret = "BUZ1r7FWxpJOswJIMrZV4FkgmOrUBC2S"  # Replace with your actual secret
                global_token = get_oauth_token(key, secret)
                # context["token"] = global_token
                # context["message"] = (
                #     "Token generated successfully!" if global_token else "Failed to generate token."
                # )
                # log_message = f"User: {user_name} - Token generation status: {'Success' if global_token else 'Failure'}"
                # logging.info(log_message)
                if global_token:
                    request.session["get_oauth_token"] = global_token  # Store token in session
                    request.session.set_expiry(3600)  # Optional: Set expiry to 1 hour (adjust as needed)
                    context["token"] = global_token
                    context["message"] = "Token generated successfully!"
                    logging.info(f"User: {user_name} - Token generated successfully!")
                else:
                    context["message"] = "Failed to generate token."
                    logging.warning(f"User: {user_name} - Token generation failed.")



            elif action == "create_batch":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestemp_prod.html", context)

                uploaded_file = request.FILES.get("file_location")
                if not uploaded_file:
                    context["message"] = "No file uploaded."
                    return render(request, "ingestemp_prod.html", context)

                headers = {
                    "Authorization": f"Bearer {global_token}",
                    "accept": "*/*",

                }
                if not os.path.exists(default_storage.location):
                    os.makedirs(default_storage.location, exist_ok=True)

                #temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
                #if not os.path.exists(default_storage.location):
                #    os.makedirs(default_storage.location)

                #with default_storage.open(temp_file_path, 'wb+') as temp_file:
                #    for chunk in uploaded_file.chunks():
                #        temp_file.write(chunk)
                try:
                    file_path = os.path.join("uploads", uploaded_file.name)
                    file_name = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                    full_file_path = default_storage.path(file_name)  # Get full path
                    logging.info(f"File saved at: {full_file_path}")


                    with open(full_file_path, 'rb') as file:
                        files = {'file': file}
                        response = requests.post(
                            "https://business.api.elsevier.com/v1/funding-ingestion/vtool",
                            headers=headers,
                            files=files,
                        )

                    if response.status_code == 200:
                        batch_id = response.json().get("batchId")
                        if batch_id:
                            context["batch_id"] = batch_id
                            context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
                            logging.info(f"User: {user_name} - Batch ID: {batch_id}")
                        else:
                            context["message"] = "Batch creation successful but no batch ID returned."
                            logging.warning(f"User: {user_name} - Batch created, but no batch ID.")
                    else:
                        context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
                        logging.error(f"User: {user_name} - Batch creation failed. Response: {response.text}")

                except PermissionError as e:
                    context["message"] = "Permission denied while saving the file."
                    logging.error(f"User: {user_name} - PermissionError: {e}")

                except Exception as e:
                    context["message"] = "An error occurred while saving the file."
                    logging.exception(f"User: {user_name} - Exception: {e}")

            # elif action == "create_batch":
            #     if not global_token:
            #         context["message"] = "Token is not available. Please generate a token first."
            #         return render(request, "ingestemp_prod.html", context)

            #     uploaded_file = request.FILES.get("file_location")
            #     if not uploaded_file:
            #         context["message"] = "No file uploaded."
            #         return render(request, "ingestemp_prod.html", context)

            #     headers = {
            #         "Authorization": f"Bearer {global_token}",
            #         "accept": "*/*",

            #     }
            #     if not os.path.exists(default_storage.location):
            #         os.makedirs(default_storage.location, exist_ok=True)

            #     # temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
            #     # if not os.path.exists(default_storage.location):
            #     #     os.makedirs(default_storage.location)

            #     # with default_storage.open(temp_file_path, 'wb+') as temp_file:
            #     #     for chunk in uploaded_file.chunks():
            #     #         temp_file.write(chunk)

            #     with open(temp_file_path, 'rb') as file:
            #         files = {'file': file}
            #         response = requests.post(
            #             "https://business.api.elsevier.com/v1/funding-ingestion/vtool",
            #             headers=headers,
            #             files=files,
                        
            #         )
                   

            #     if response.status_code == 200:
            #         batch_id = response.json().get("batchId")
            #         if batch_id:
            #             context["batch_id"] = batch_id
            #             context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
            #             log_message = f"User: {user_name} - Batch created successfully! Batch ID: {batch_id}"
            #             logging.info(log_message)
            #         else:
            #             context["message"] = "Batch creation successful but no batch ID returned."
            #             logging.warning(f"User: {user_name} - Batch creation successful but no batch ID returned.")
            #     else:
            #         context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
            #         logging.error(f"User: {user_name} - Failed to create batch. Response Code: {response.status_code}")

            elif action == "ingest_file":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestemp_prod.html", context)

                ingestion_type = form.cleaned_data["ingestion_type"]
                batch_id = request.POST.get("batch_id")
                file = request.FILES.get("json_location")
                data_type = form.cleaned_data["data_type"]

                if not file:
                    context["message"] = "No file provided for ingestion."
                    return render(request, "ingestemp_prod.html", context)

                base_url = "https://business.api.elsevier.com/v1/funding-ingestion"
                url = f"{base_url}/{data_type}"
                if ingestion_type == "batch":
                    url += "/bulk"

                headers = {
                    "accept": "application/json",
                    "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
                    "Content-Type": "application/json",
                    "batchId": batch_id,
                    "Authorization": f"Bearer {global_token}",
                }

                try:
                    response = requests.post(url, headers=headers, data=file.read())
                    ingestion_response = response.json()

                    ingestion_id = ingestion_response.get("ingestionId")
                    ingestion_item_id = ingestion_response.get("id")

                    if ingestion_id and ingestion_item_id:
                        log_message = (
                            f"User: {user_name} - Timestamp: {datetime.now()} - "
                            f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
                        )
                        logging.info(log_message)
                        
                        # Store details in the database
                        reserve_ingestion_log(user_name, ingestion_id, ingestion_item_id, batch_id)

                    if response.status_code == 200:
                        context["message"] = "File ingested successfully!"
                    else:
                        context["message"] = f"Failed to ingest file: {response.text}"
                        logging.error(f"User: {user_name} - Failed to ingest file: {response.text}")

                except Exception as e:
                    context["message"] = "An error occurred during file ingestion."
                    logging.exception(f"User: {user_name} - Exception occurred during file ingestion: {e}")
                    
 # Step 5: Check Ingestion Status
            elif action == "check_ingestion_status":
                ingestion_id = request.POST.get("ingestion_id")
                data_type = request.POST.get("data_type")

                if not ingestion_id:
                    context["ingestion_status_message"] = "Please provide an ingestion ID."
                    return render(request, "ingestemp_prod.html", context)

                base_urls = {
                    "award": "https://business.api.elsevier.com/v1/funding-ingestion/award/",
                    "opportunity": "https://business.api.elsevier.com/v1/funding-ingestion/opportunity/",
                    "funding-body": "https://business.api.elsevier.com/v1/funding-ingestion/funding-body/"
                }

                url = f"{base_urls[data_type]}{ingestion_id}"
                headers = {"accept": "application/json", "Authorization": f"Bearer {global_token}"}

                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        response_data = response.json()
                        context["ingestion_status_message"] = f"Status: {response_data.get('status', 'Unknown')}"
                    else:
                        context["ingestion_status_message"] = f"Failed to fetch status. Response Code: {response.status_code}"
                except Exception as e:
                    context["ingestion_status_message"] = "An error occurred while checking ingestion status."
                    logging.exception(f"User: {user_name} - Exception during status check: {e}")
                    context["ingestion_status_message"] = "Failed to fetch status."

    return render(request, "ingestemp_prod.html", context)
    



################view code for storing imgestion details in db  ##########

def reserve_ingestion_log(user_name, ingestion_id, ingestion_item_id, batch_id):
    """Store ingestion details in the database."""
    IngestProd.objects.create(
        user_name=user_name,
        ingestion_id=ingestion_id,
        ingestion_item_id=ingestion_item_id,
        batch_id=batch_id,
        status="Success"  # Initially set status as Success, update if needed
    )

####################code for displaying ingestion details in table view in ui##################################
from django.shortcuts import render
from .models import IngestProd

@login_required
def ingest_prod_view(request):
    """Fetch all ingestion logs and render them in a table UI."""
    ingest_logs = IngestProd.objects.all()  # Get logs sorted by latest entries

    context = {
        "ingest_logs": ingest_logs
    }
    return render(request, "ingest_prod_logs.html", context) 



##############################################################################################

from django.contrib.auth.models import User  # If using a custom user model, import that
from django.shortcuts import render

@login_required
def user_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'users_list.html', {'users': users})


###########################ending view of ingestion ###############################################################



# ################################# view for dashbaord##############################
from django.contrib.auth.models import User
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from collections import defaultdict
import base64
from .models import SourceMetadata,IngestionLog
from .models import IngestProd
@login_required
def dashboard_view(request):
    # Fetch all source metadata records from MongoDB
    source_metadata_list = SourceMetadata.objects.all()

    # Fetch count of successfully ingested files
    total_ingested_files = IngestionLog.objects.filter(status="Success").count()

    # Fetch count of successfully ingested files in prod
    ingest_prod_files = IngestProd.objects.filter(status="Success").count()



    # Convert QuerySet to list of dictionaries manually
    data = []
    for item in source_metadata_list:
        data.append({
            'import_url': item.import_url,
            'date_of_arrival': item.date_of_arrival,
            'assigned_to': item.assigned_to,
            'frequency_of_site_updates': item.frequency_of_site_updates,
            'site_last_checked': item.site_last_checked,
            'source_file_upload': item.source_file_upload,
            'json_file_name': item.json_file_name,
            'json_upload_date': item.json_upload_date,
            'sup_id': item.sup_id,
            'sme_comments': item.sme_comments,
            'screenshots_taken': item.screenshots_taken,
            'qa_comment': item.qa_comment,
            'qa_name': item.qa_name,
            'file_status': item.file_status,
            'qa_issue': item.qa_issue,
            'created_at': item.created_at,
        })

    # Convert the data to a Pandas DataFrame for easy processing
    df = pd.DataFrame(data)

    # Initialize variables for dashboard metrics
    total_sources = total_files = qa_pending  = in_progress_tasks = 0     #= completed_tasks
    accepted_files = rejected_files = 0
    user_metrics = defaultdict(lambda: {
        'total_files': 0,
        'accepted': 0,
        'rejected': 0,
        'in_progress': 0,
        'reprocessing': 0,
        'qa_name': None,
    })

    # Calculate metrics if the DataFrame is not empty
    if not df.empty:
        total_sources = len(df)
        total_files = df['source_file_upload'].notna().sum()
        qa_pending = df[df['file_status'] == 'Pending'].shape[0]
        # completed_tasks = df[df['file_status'] == 'Completed'].shape[0]
        in_progress_tasks = df[df['file_status'] == 'In Progress'].shape[0]

        # Calculate Accepted and Rejected Files
        accepted_files = df[df['file_status'] == 'Accepted'].shape[0]
        rejected_files = df[df['file_status'] == 'Rejected'].shape[0]

        # Prepare user-specific metrics
        for _, row in df.iterrows():
            user = row['assigned_to']
            user_metrics[user]['total_files'] += 1
            user_metrics[user]['qa_name'] = row['qa_name']

            if row['file_status'] == 'Accepted':
                user_metrics[user]['accepted'] += 1
            elif row['file_status'] == 'Rejected':
                user_metrics[user]['rejected'] += 1
            elif row['file_status'] == 'In Progress':
                user_metrics[user]['in_progress'] += 1
            elif row['file_status'] == 'Reprocessing':
                user_metrics[user]['reprocessing'] += 1

        # Prepare the data for chart (Tasks per User)
        user_task_counts = df['assigned_to'].value_counts()

        # Create Matplotlib chart (Bar Chart) for Tasks per User
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.bar(user_task_counts.index, user_task_counts.values, color='#f5a142')

        ax.set_xlabel('Users')
        ax.set_ylabel('Number of Tasks')
        ax.set_title('Tasks per User')

        # Save the bar chart to a BytesIO object to embed it in the HTML
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        buf.seek(0)
        chart_data = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Create Pie Chart for User Work Distribution
        user_work_distribution = user_task_counts.values
        user_labels = user_task_counts.index

        # Create Pie Chart
        fig_pie, ax_pie = plt.subplots(figsize=(6.5, 6.5))
        ax_pie.pie(user_work_distribution, labels=user_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the pie chart to a BytesIO object to embed it in the HTML
        buf_pie = BytesIO()
        fig_pie.savefig(buf_pie, format='png')
        buf_pie.seek(0)
        pie_chart_data = base64.b64encode(buf_pie.read()).decode('utf-8')
        buf_pie.close()

    # Count total users
    total_users = User.objects.count()

    context = {
        'total_sources': total_sources,
        'total_files': total_files,
        'qa_pending': qa_pending,
        # 'completed_tasks': completed_tasks,
        'ingest_prod_files':ingest_prod_files,
        'in_progress_tasks': in_progress_tasks,
        'accepted_files': accepted_files,
        'rejected_files': rejected_files,
        'chart_data': chart_data,  # Bar chart
        'pie_chart_data': pie_chart_data,  # Pie chart
        'user_metrics': user_metrics.items(),  # Ensure items() is passed
        'total_users': total_users,  # Include total users
        'total_ingested_files': total_ingested_files,  # Include ingested file count
    }

    return render(request, 'dashboard.html', context)





#json creation view code
# import os
# import json
# from django.shortcuts import render
# from .forms import CSVInputForm
# from .utils import s_date,format_date,generate_small_hash_uuid,generate_small_hash_AID,get_and_update_ids,process_csv_to_json # Assuming you have these functions defined
 
# def upload_file(request):
#     if request.method == 'POST':
#         form = CSVInputForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file_path = form.cleaned_data['csv_file_path']
#             output_directory = form.cleaned_data['output_directory']
 
#             # Ensure the output directory exists
#             os.makedirs(output_directory, exist_ok=True)
 
#             # Process the provided CSV file path
#             json_filename = os.path.splitext(os.path.basename(csv_file_path))[0] + '.json'
#             json_output_path = os.path.join(output_directory, json_filename)
 
#             # Process the CSV and generate JSON
#             process_csv_to_json(csv_file_path, json_output_path)
 
#             # Read the generated JSON file and clean it (if you have clean_data defined)
#             with open(json_output_path, 'r', encoding='utf-8-sig') as file:
#                 data = json.load(file)
 
#             cleaned_data = clean_data(data)  # Assuming this function is defined elsewhere
#             final_data = remove_outermost(cleaned_data)  # Assuming this function is defined elsewhere
#             # Save cleaned JSON data to a new file
#             cleaned_json_filename = os.path.splitext(json_filename)[0] + '_N.json'
#             cleaned_json_output_path = os.path.join(output_directory, cleaned_json_filename)
#             with open(cleaned_json_output_path, 'w', encoding='utf-8') as file:
#                 json.dump(final_data, file, ensure_ascii=False, separators=(',', ':'))
 
#             return render(request, 'upload_file.html', {'form': form, 'success': True,
#                                                              'cleaned_json_path': cleaned_json_output_path})
#     else:
#         form = CSVInputForm()
#     return render(request, 'upload_file.html', {'form': form})

#json creator  code ##############################

import os
import json
from django.shortcuts import render
from .forms import CSVInputForm
from .utils import process_csv_to_json
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = CSVInputForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']  # Get the uploaded file
            output_directory = form.cleaned_data['output_directory']

            os.makedirs(output_directory, exist_ok=True)  # Ensure output directory exists

            # Save the uploaded file to the output directory
            csv_file_path = os.path.join(output_directory, csv_file.name)
            with open(csv_file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Process the CSV file
            json_filename = os.path.splitext(csv_file.name)[0] + '.json'
            json_output_path = os.path.join(output_directory, json_filename)

            process_csv_to_json(csv_file_path, json_output_path)

            return render(request, 'upload_file.html', {'form': form, 'success': True, 'cleaned_json_path': json_output_path})
    else:
        form = CSVInputForm()

    return render(request, 'upload_file.html', {'form': form})


################ending the json creator code#####################
#####################################################################



################# v tool code ##########################
#########################################################################
from django.contrib import messages
from django.views.decorators.http import require_POST
import subprocess 

@require_POST
@login_required
def run_java_tool(request):
    json_file = request.POST.get('json_file')
    log_file = request.POST.get('log_file')
   
   
    # Define the command. Adjust the path to your Vtool.jar accordingly.
    command = [
        'java',
        '-jar',
        r' X:\json_project_1\Vtool-5.93.1-p1\Vtool.jar',
        '--vjson', 'grant',
        '-file', json_file,
        '-log', log_file
    ]
   
    try:
        # Run the command and capture the output (if needed)
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        messages.success(request, f"Tool ran successfully. Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        messages.error(request, f"Error running tool: {e.stderr}")
   
    return redirect('qa_process')
