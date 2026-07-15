from ingest import extraction
import re
Section_headers = ["EXPERIENCE", "PROJECTS", "EDUCATION", "SKILLS"]

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



text = extraction()
result = split_into_sections(text)
print(result.keys())
entries = chunking_experience(result["EXPERIENCE"])
print(len(entries))
print(entries[0])