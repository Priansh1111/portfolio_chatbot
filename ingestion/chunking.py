from ingest import extraction
import re
Section_headers = ["EXPERIENCE", "PROJECTS", "EDUCATION", "TECHNICAL SKILLS", "EXTRA CURRICULARS"]

def split_into_sections(text):
    lines = [l for l in text.split("\n") if l.strip()]

    sections = {}

    current_header = "Header"
    buffer = []

    for line in lines:
        if line.strip() in Section_headers:
            sections[current_header] = "\n".join(buffer).strip()
            current_header = line.strip()
            buffer = []

        else:
            buffer.append(line)

    sections[current_header] = "\n".join(buffer).strip()   
    return sections    
    
def chunking_experience(text):
    date_pattern = re.compile(r"[A-Z][a-z]{2} \d{4}\s*-\s*[A-Z][a-z]{2} \d{4}")
    lines = [l for l in text.split("\n") if l.strip()]   # <-- this line was missing

    entries = []
    current = []

    for line in lines:
        if date_pattern.search(line) and current:
            entries.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        entries.append(current)

    return entries



# text = extraction()
# result = split_into_sections(text)
# print(result.keys())
# entries = chunking_experience(result["EXPERIENCE"])
# print(len(entries))
# print(entries[0])


def chunk_projects(text):

    lines = [l for l in text.split("\n") if l.strip()]
    entries = []
    current = []

    for line in lines:
        if "|" in line and current:
            entries.append(current)
            current = [line]

        else:
            current.append(line)

    if current:
        entries.append(current)

    return entries


# text = extraction()
# result = split_into_sections(text)
# entries = chunk_projects(result["PROJECTS"])
# print(len(entries))
# print(entries[1])

def chunk_education(text):
    text = text.strip()
    return [{
        "content": text,
        "section": "education",
        "entry_name": "education"
    }]

SKILL_CATEGORIES = ["Languages", "Frameworks & Libraries", "AI Architectures & Concepts", "Database", "Tools"]

def chunk_skills(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    entries = []
    current_category = None
    current_lines = []

    for line in lines:
        matched_category = None
        for category in SKILL_CATEGORIES:
            if line.startswith(category):
                matched_category = category
                break

        if matched_category:
            if current_category:
                entries.append((current_category, current_lines))
            current_category = matched_category
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_category:
        entries.append((current_category, current_lines))

    chunks = []
    for category, entry_lines in entries:
        chunks.append({
            "content": " ".join(entry_lines),
            "section": "skills",
            "entry_name": category.lower()
        })
    return chunks

def chunk_extracurriculars(text):
    text = text.strip()
    return [{
        "content": text,
        "section": "extracurricular",
        "entry_name": "extracurriculars"
    }]

def chunk_resume(text):
    sections = split_into_sections(text)
    chunks = []

    experience_entries = chunking_experience(sections["EXPERIENCE"])
    for entry in experience_entries:
        chunks.append({
            "content": "\n".join(entry),
            "section": "experience",
            "entry_name": entry[0]
        })

    project_entries = chunk_projects(sections["PROJECTS"])
    for entry in project_entries:
        chunks.append({
            "content": "\n".join(entry),
            "section": "project",
            "entry_name": entry[0].split("|")[0].strip()
        })

    chunks.extend(chunk_education(sections["EDUCATION"]))
    chunks.extend(chunk_skills(sections["TECHNICAL SKILLS"]))
    chunks.extend(chunk_extracurriculars(sections["EXTRA CURRICULARS"]))

    return chunks

text = extraction()
all_chunks = chunk_resume(text)
print(len(all_chunks))       
for c in all_chunks:
    print(c["section"], "|", c["entry_name"])