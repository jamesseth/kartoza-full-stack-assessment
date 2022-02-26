"""File upload form implementation."""
from django import forms


# The UploadFileForm class inherits from forms.Form.
#
# The class has two fields: title and file.
#
# The title field is a CharField with a max length of 127.
#
# The file field is a FileField
class UploadFileForm(forms.Form):
    """Implement a file upload form."""

    title = forms.CharField(max_length=127)
    file = forms.FileField()
