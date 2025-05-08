import requests
from PIL import Image
import os


def download(pages, path):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    os.makedirs(path, exist_ok=True)  # 自动创建目标目录

    for i in range(1, pages + 1):
        url = f'https://s3.ananas.chaoxing.com/sv-w9/doc/e1/61/ed/f90f483d07030e34b0cfc004ffacffc6/thumb/{i}.png'
        try:
            response = requests.get(url, headers=header, timeout=10)
            response.raise_for_status()  # 自动检测4xx/5xx错误

            # 验证内容是否为图片
            if 'image' not in response.headers.get('Content-Type', ''):
                print(f"URL {url} 返回非图片内容")
                continue

            # 保存文件
            with open(os.path.join(path, f"{i}.png"), 'wb') as f:
                f.write(response.content)
            print(f"成功下载第 {i} 页")

        except Exception as e:
            print(f"下载第 {i} 页失败: {str(e)}")


def turnpic2pdf(path, name):
    img_list = []
    files = sorted(os.listdir(path), key=lambda x: int(x.split('.')[0]))

    for filename in files:
        filepath = os.path.join(path, filename)
        try:
            img = Image.open(filepath)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_list.append(img)
        except Exception as e:
            print(f"无法打开 {filename}: {str(e)}")
            continue

    if not img_list:
        print("没有有效图片可转换")
        return

    pdf_path = os.path.join(os.path.dirname(path), f"{name}.pdf")
    img_list[0].save(
        pdf_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=img_list[1:]
    )
    print(f"PDF已保存至 {pdf_path}")


if __name__ == '__main__':
    save_path = "C:/Users/oybl/OneDrive/桌面/计组课件/课件"
    total_pages = 48
    pdf_name = '课件8'

    download(total_pages, save_path)
    turnpic2pdf(save_path, pdf_name)