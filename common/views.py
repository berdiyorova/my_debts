from django.shortcuts import render

def get_page_and_page_size(request):
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 3))
    except ValueError:
        raise Exception('page and page size must be integer')
    return page, page_size
