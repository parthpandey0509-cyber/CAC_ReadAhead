import pymupdf as pmp
def convert_read(file):
    file_ext = file.name.split('.')[-1].lower()
    doc=pmp.open(stream=file.getvalue(), filetype=file_ext)
    return [page.get_text() for page in doc]




