import os 

def delete_existing_files():
    if os.path.exists('crawl_output.jl'):
        os.remove('crawl_output.jl')
    if os.path.exists('output_file.log'):
        os.remove('output_file.log')


def validate_links(links):
    if not links.startswith("http"):
        raise ValueError("The URL is invalid")
        return False
    else:
        return True