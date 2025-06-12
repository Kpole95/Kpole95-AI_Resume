import re
import logging
from docx import Document
from langdetect import detect, LangDetectException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADER_MAPPING = {
    "contact_info": ["contact", "contact info", "contact information", "personal details", "контакты", "контактная информация"],
    "summary": ["summary", "objective", "professional summary", "career objective", "о себе", "профиль", "цель"],
    "experience": ["experience", "work experience", "professional experience", "employment history", "опыт работы"],
    "education": ["education", "academic background", "qualifications", "образование"],
    "skills": ["skills", "technical skills", "technical proficiencies", "key skills", "core competencies", "навыки", "ключевые навыки", "технические навыки"],
    "certifications": ["certifications", "licenses", "courses", "сертификаты", "курсы", "лицензии"],
    "projects": ["projects", "personal projects", "academic projects", "проекты"],
    "publications": ["publications", "articles", "papers", "публикации"],
    "languages": ["languages", "language proficiency", "языки", "знание языков"],
    "interests": ["interests", "hobbies", "увлечения", "хобби"],
    "awards": ["awards & honors", "awards", "honors", "награды и поощрения", "награды"],
    "volunteer_experience": ["volunteer experience", "volunteering", "волонтерский опыт"],
    "affiliations": ["professional affiliations", "memberships", "профессиональное членство"],
    "conferences": ["conferences", "workshops", "conferences / workshops", "конференции", "семинары"],
    "portfolio": ["portfolio", "github", "portfolio / github", "портфолио"],
    "references": ["references", "рекомендации"],
}

SKILL_DATABASE = [
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'ruby', 'php', 'swift', 'kotlin', 'go', 'html5', 'css3', 'react', 'angular',
    'vue.js', 'node.js', 'express.js', 'django', 'flask', 'spring boot', 'sql', 'mysql', 'postgresql', 'mongodb', 'oracle database',
    'microsoft sql server', 'redis', 'aws', 'amazon web services', 'microsoft azure', 'azure', 'google cloud platform', 'gcp', 'docker',
    'kubernetes', 'jenkins', 'terraform', 'ansible', 'puppet', 'ci/cd', 'ci/cd pipelines', 'microservices architecture', 'microservices',
    'restful apis', 'graphql', 'mobile development', 'android', 'ios', 'react native', 'flutter', 'xamarin', 'cybersecurity',
    'penetration testing', 'network security', 'cryptography', 'encryption', 'firewall configuration', 'firewall', 'software testing',
    'manual testing', 'automated testing', 'selenium', 'junit', 'testng', 'mockito', 'behavior driven development', 'bdd', 'git', 'github',
    'gitlab', 'bitbucket', 'agile', 'scrum', 'kanban', 'agile methodologies', 'software development life cycle', 'sdlc',
    'object-oriented programming', 'oop', 'functional programming', 'design patterns', 'uml', 'devops', 'devops practices',
    'r', 'sql', 'nosql', 'hadoop', 'spark', 'hive', 'kafka', 'tableau', 'power bi', 'looker', 'd3.js', 'matplotlib', 'seaborn',
    'plotly', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'natural language processing', 'nlp', 'computer vision',
    'predictive modeling', 'statistical analysis', 'regression analysis', 'regression', 'hypothesis testing', 'data cleaning',
    'data wrangling', 'etl', 'big data', 'big data technologies', 'aws redshift', 'redshift', 'google bigquery', 'bigquery',
    'data warehousing', 'a/b testing', 'data mining', 'business intelligence', 'bi', 'pandas', 'numpy', 'scipy', 'machine learning',
    'data science', 'deep learning', 'data analysis', 'financial reporting', 'budgeting & forecasting', 'budgeting', 'forecasting',
    'variance analysis', 'tax preparation', 'regulatory compliance', 'sox', 'gaap', 'ifrs', 'auditing', 'risk management', 'investment analysis',
    'treasury management', 'treasury', 'payroll management', 'payroll', 'accounts payable', 'accounts receivable', 'quickbooks', 'sap financials',
    'oracle financials', 'microsoft excel', 'advanced excel', 'excel', 'financial modeling', 'cash flow management', 'erp systems', 'erp',
    'credit analysis', 'banking software', 'finacle', 'fis', 'seo', 'search engine optimization', 'sem', 'search engine marketing', 'google analytics',
    'google ads', 'adwords', 'social media marketing', 'facebook marketing', 'instagram marketing', 'linkedin marketing', 'twitter marketing',
    'content marketing', 'copywriting', 'email marketing', 'mailchimp', 'constant contact', 'marketing automation', 'hubspot', 'marketo', 'crm software',
    'crm', 'salesforce', 'zoho crm', 'microsoft dynamics', 'lead generation', 'sales funnel management', 'account management', 'market research',
    'branding', 'event planning', 'product marketing', 'negotiation', 'customer relationship management', 'telemarketing', 'direct sales', 'channel sales',
    'patient care', 'medical terminology', 'hipaa compliance', 'hipaa', 'electronic health records', 'ehr', 'clinical trials management',
    'clinical trials', 'medical coding', 'icd', 'cpt', 'pharmacology', 'cpr', 'bls', 'laboratory techniques', 'medical imaging', 'mri',
    'x-ray', 'ct scan', 'research protocols', 'epidemiology', 'healthcare quality assurance', 'clinical data management', 'patient scheduling',
    'telemedicine', 'healthcare billing', 'agile methodologies', 'scrum', 'kanban', 'waterfall', 'risk management', 'resource allocation',
    'budget management', 'microsoft project', 'jira', 'trello', 'asana', 'confluence', 'project scheduling', 'stakeholder management',
    'change management', 'quality assurance', 'scope management', 'communication planning', 'earned value management', 'evm', 'pmp',
    'adobe photoshop', 'photoshop', 'adobe illustrator', 'illustrator', 'adobe indesign', 'indesign', 'sketch', 'figma', 'ux/ui design',
    'ux', 'ui', 'wireframing', 'prototyping', 'animation', 'after effects', 'blender', 'video editing', 'premiere pro', 'final cut pro',
    'branding', 'typography', 'color theory', '3d modeling', 'maya', '3ds max', 'graphic design', 'print design', 'digital illustration',
    'communication', 'teamwork', 'leadership', 'problem solving', 'time management', 'critical thinking', 'adaptability', 'creativity',
    'conflict resolution', 'collaboration', 'emotional intelligence', 'decision making', 'negotiation', 'multitasking', 'attention to detail',
    'work ethic', 'customer service', 'coaching', 'mentoring', 'presentation skills', 'english', 'spanish', 'mandarin', 'french', 'german',
    'japanese', 'hindi', 'arabic', 'russian', 'portuguese', 'foreign language proficiency', 'technical writing', 'public speaking',
    'grant writing', 'teaching', 'training', 'event coordination', 'supply chain management', 'logistics', 'quality control',
    'environmental health & safety', 'ehs', 'legal research', 'contract negotiation'
]

def extract_resume_data(file_path: str) -> dict:
    try:
        doc = Document(file_path)
        full_text_lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(full_text_lines)
        all_headers_to_standard_key = {
            header.upper(): standard_key
            for standard_key, header_list in HEADER_MAPPING.items() for header in header_list
        }
        parsed_sections = {"header": []}
        current_section_key = "header"
        for line in full_text_lines:
            line_upper = line.upper()
            is_header = False
            if line_upper in all_headers_to_standard_key and len(line.split()) < 5:
                current_section_key = all_headers_to_standard_key[line_upper]
                is_header = True
            elif len(line.split()) <= 5 and not line.endswith('.') and (line.isupper() or line.istitle()):
                current_section_key = line.lower().replace(" ", "_").replace("&", "and")
                is_header = True
            if is_header and current_section_key not in parsed_sections:
                parsed_sections[current_section_key] = []
            elif not is_header:
                parsed_sections[current_section_key].append(line)
        final_data = {
            key: "\n".join(content).strip() for key, content in parsed_sections.items() if content
        }
        final_data['found_skills'] = sorted(list({
            skill.title() for skill in SKILL_DATABASE
            if re.search(r'\b' + re.escape(skill) + r'\b', full_text, re.IGNORECASE)
        }))
        try:
            final_data['detected_language'] = detect(full_text)
        except LangDetectException:
            final_data['detected_language'] = 'unknown'
        
        # --- FIX #3: Final, simpler Name Detection ---
        final_data['name'] = final_data.get('header', '').split('\n')[0] if final_data.get('header') else "N/A"
            
        logger.info(f"parser successfully extracted {len(final_data)} sections.")
        return final_data
    except Exception as e:
        logger.error(f"A critical error occurred in the universal parser for file {file_path}: {str(e)}")
        raise RuntimeError(f"Could not parse the resume. The file may be corrupted or in an unsupported format. Details: {str(e)}")