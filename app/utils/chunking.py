Section_headers = ["EXPERIENCE", "PROJECTS", "EDUCATION", "SKILLS"]

def split_into_sections(text):
    lines = text.split("\n")

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