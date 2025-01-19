import os
from web.models import DocxFile
from django.core.files import File
from django.db import IntegrityError

def upload_docx_files(folder_path):
    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} không tồn tại!")
        return
    
    # Duyệt qua tất cả các file trong thư mục
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            
            # Lấy tên file mà không có phần mở rộng .docx
            title = os.path.splitext(filename)[0]
            
            # Kiểm tra nếu file đã tồn tại trong cơ sở dữ liệu
            if DocxFile.objects.filter(title=title).exists():
                print(f"File {title} đã tồn tại trong cơ sở dữ liệu.")
                continue  # Bỏ qua file này và tiếp tục với file khác
            
            try:
                # Mở file và lưu vào cơ sở dữ liệu
                with open(file_path, 'rb') as f:
                    docx_file = DocxFile(name=filename, title=title)
                    docx_file.file.save(filename, File(f), save=True)
                    print(f"File {filename} đã được tải lên thành công.")
            except IntegrityError:
                print(f"Lỗi IntegrityError khi tải lên file {filename}.")
            except Exception as e:
                print(f"Đã xảy ra lỗi khi tải lên file {filename}: {e}")

# Gọi hàm để upload file từ thư mục vào cơ sở dữ liệu
upload_docx_files('/workspaces/project2024/prj/test')
