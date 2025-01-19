from django.shortcuts import render, get_object_or_404
from .models import DocxFile
from django.db.models import Q
import os
from django.http import FileResponse
import pypandoc

# Create your views here.
def main(request):
    context = {}
    return render(request, 'web/main.html', context)

def home(request):
    context = {}
    return render(request, 'web/home.html', context)

def chat(request):
    context = {}
    return render(request, 'web/chat.html', context)

def blog(request):
    context = {}
    return render(request, 'web/blog.html', context)

def convert_docx_to_pdf(docx_path, pdf_path):
    output = pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path)
    assert output == ""
    return pdf_path

def category_list(request):
    query = request.GET.get('q', '')
    files = DocxFile.objects.filter(name__icontains=query)
    return render(request, 'web/category_list.html', {'files': files, 'query': query})

def file_detail(request, file_id):
    docx_file = get_object_or_404(DocxFile, id=file_id)
    
    # Đường dẫn đến file DOCX
    docx_path = docx_file.file.path
    
    # Tạo đường dẫn PDF
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    
    # Kiểm tra xem file PDF đã tồn tại chưa, nếu chưa thì chuyển đổi từ DOCX
    if not os.path.exists(pdf_path):
        convert_docx_to_pdf(docx_path, pdf_path)
    
    # Trả về file PDF cho người dùng
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')