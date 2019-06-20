from . import converter

def run():
    if file_filetype == "ttl":
        converter.convert(file_destination, corpus_dir, file_name)
