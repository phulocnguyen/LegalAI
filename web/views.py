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

from django.shortcuts import render
from django.http import JsonResponse
from .ai_service import basicrag  # Import đối tượng basicrag từ ai_service.py

def chat_with_ai_view(request):
    if request.method == "POST":
        question = request.POST.get("question")

        # Kiểm tra nếu question rỗng
        if not question:
            return JsonResponse({"error": "Câu hỏi không được để trống."}, status=400)

        # Sử dụng basicrag để lấy câu trả lời
        try:
            answer = basicrag.answer(question=question)
            #answer = "Đây là câu tra lời của bạn"
            
            return JsonResponse({"question": question, "answer": answer})
        except Exception as e:
            return JsonResponse({"error": f"Lỗi trong quá trình xử lý: {str(e)}"}, status=500)

    return render(request, "web/chat.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

def account(request):
    # Form đăng ký và đăng nhập
    signup_form = SignUpForm()
    login_form = AuthenticationForm()

    # Xử lý đăng ký khi người dùng submit form đăng ký
    if request.method == 'POST' and 'sign-up' in request.POST:
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            #login(request, user)  # Đăng nhập ngay sau khi đăng ký thành công
            messages.success(request, "Account created successfully! Please Login")
            return redirect('account')
        else:
            messages.error(request, "There was an error with your signup.")

    # Xử lý đăng nhập khi người dùng submit form đăng nhập
    elif request.method == 'POST' and 'sign-in' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.success(request, f"Welcome back, {username}!")
                request.session['logged_in'] = True
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    # Render trang account với cả hai form đăng ký và đăng nhập
    context = {'signup_form': signup_form, 'login_form': login_form}
    return render(request, 'web/account.html', context)

def logout_view(request):
    logout(request)
    request.session['logged_in'] = False
    return redirect('/')  # Chuyển hướng sau khi đăng xuất

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

def home(request):
    posts = Post.objects.all()
    post_form = PostForm()
    return render(request, 'web/home.html', {'posts': posts, 'post_form': post_form})

@login_required(login_url='/account')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'status': 'success', 'post_id': post.id})
    return JsonResponse({'status': 'error'})

def search_posts(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    return render(request, 'web/partials/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, 'web/partials/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

import logging
logger = logging.getLogger(__name__)


@login_required(login_url='/account')
def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Bạn cần đăng nhập để thêm bình luận.'}, status=403)
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Lấy lại danh sách bình luận mới nhất
            comments = post.comments.all().order_by('-created_at')
            comments_data = [{
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for comment in comments]

            return JsonResponse({'status': 'success', 'message': 'Bình luận đã được thêm thành công!', 'comments': comments_data})

        return JsonResponse({'status': 'error', 'message': 'Đã xảy ra lỗi. Vui lòng thử lại.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ.'}, status=400)