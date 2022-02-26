"""Implementation of upload file view."""
from django.http import HttpResponseRedirect
from django.shortcuts import render

from kartoza.file_upload.file_upload_handler import handle_uploaded_file
from kartoza.file_upload_form import UploadFileForm


def upload_file(request):
    """
    Render upload file form.

    :param request: The HTTP request.
    :return: A rendered HTML page.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
