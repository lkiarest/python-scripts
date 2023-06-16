# 保存图片中的 pdf 图片
import io
import sys
import PyPDF2
from PIL import Image, ImageChops

args = sys.argv

def exportImg(file_path):
  # 打开PDF文件
  pdf_file = open(file_path, 'rb')
  pdf_reader = PyPDF2.PdfReader(pdf_file)

  # 遍历PDF中的每一页
  for page_num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[page_num]

      # 获取当前页中的所有图片，返回第一个查找到的图片
      xObject = page['/Resources']['/XObject'].get_object()
      for obj in xObject:
          if xObject[obj]['/Subtype'] == '/Image':
              # 获取图片的信息
              size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
              data = xObject[obj]._data
              print(size)
              if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                  mode = "RGB"
              elif xObject[obj]['/ColorSpace'] == '/DeviceGray':
                  mode = "L"
              else:
                  mode = "CMYK"
              # 打开图像数据并转换为 RGB 模式
              img = Image.open(io.BytesIO(data)).convert(mode)
              # 如果图像不是 RGB 模式，则转换为 RGB 模式
              if mode != "RGB":
                  img = img.convert("RGB")
              save_name = 'exported.jpg'
              img.save(save_name)

              return save_name


def compareImg(img_path1, img_path2):
  # 打开两个图片文件
  image1 = Image.open(img_path1)
  image2 = Image.open(img_path2)

  # 比较两个图片是否相同
  if image1.size == image2.size and image1.mode == image2.mode:
      difference = ImageChops.difference(image1, image2)
      if not difference.getbbox():
          print("两个图片相同")
      else:
          # 显示差异的部分
          bbox = difference.getbbox()
          image1_crop = image1.crop(bbox)
          image2_crop = image2.crop(bbox)
          image1_crop.show()
          image2_crop.show()
  else:
      print("两个图片大小不同")


def run():
  exported_img = exportImg(args[1])
  to_compare = args[2]
  compareImg(exported_img, to_compare)


run()
