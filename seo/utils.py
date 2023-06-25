import os


def delete_existing_files():
    if os.path.exists("output/crawl_output.jl"):
        os.remove("output/crawl_output.jl")
    if os.path.exists("logs/crawlLogs/output_file.log"):
        os.remove("logs/crawlLogs/output_file.log")


def validate_links(links):
    if not links.startswith("http"):
        raise ValueError("The URL is invalid")
        return False
    else:
        return True
