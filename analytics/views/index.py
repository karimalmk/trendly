from django.shortcuts import render

# =============================================
# INDEX VIEW
# =============================================
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    initial = request.user.username[0].upper() if request.user.is_authenticated else ""
    return render(request, "index.html")