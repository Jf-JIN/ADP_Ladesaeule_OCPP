import fitz  # PyMuPDF
import fitz
import base64
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QByteArray

pdf_path = 'E:/10_Programm/0002_Python/0903_ADP_Ladesaeule_OCPP/github/python_script/test/EVSE_Test/evse-wb-din_latest.pdf'


# doc = fitz.open(pdf_path)
# result = []
# for i in range(len(doc)):
#     page = doc[i]
#     pix = page.get_pixmap(alpha=False)

#     image_bytes = pix.tobytes("png")  # 使用 PNG 格式
#     base64_str = base64.b64encode(image_bytes).decode("utf-8")
#     result.append(base64_str)

# with open('output.py', 'w', encoding='utf-8') as f:
#     f.write(f'PDF_PAGES = ' + str(result))


# doc = fitz.open(pdf_path)
# result = []
# for i in range(len(doc)):
#     page = doc[i]
#     pix = page.get_pixmap(alpha=False)

#     image_bytes = pix.tobytes("png")  # 使用 PNG 格式
#     base64_str = base64.b64encode(image_bytes).decode("utf-8")
#     result.append(base64_str)

# # 输出到 Python 文件
# with open('const/Const_PDF.py', 'w', encoding='utf-8') as f:
#     f.write('PDF_PAGES = [\n')
#     for page in result:
#         f.write(f'    "{page}",\n')
#     f.write(']\n')


doc = fitz.open(pdf_path)
result = []

zoom = 2.0  # 放大倍数（1.0 = 原始大小，2.0 = 2倍分辨率）
mat = fitz.Matrix(zoom, zoom)

for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(matrix=mat, alpha=False)  # 使用放大矩阵
    image_bytes = pix.tobytes("png")  # PNG格式
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    result.append(base64_str)

# 输出到 Python 文件
with open('const/Const_PDF.py', 'w', encoding='utf-8') as f:
    f.write('PDF_PAGES = [\n')
    for page in result:
        f.write(f'    "{page}",\n')
    f.write(']\n')
