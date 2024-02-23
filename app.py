import requests,io
from flask import Flask, request, send_file
from PIL import Image

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 处理图片-尺寸修改
# @app.route('/image/<path:image_path>', methods =['GET'])
def get_image(url):
    # 从 MinIO 服务中获取原始图片
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise RuntimeError("获取图片失败")

    # 使用 Pillow 库来打开图片
    image = Image.open(response.raw)
    print(image.size,image.format,image.width,image.height)
    return image

def handle_image_size(image, width, height):
    # 修改图片大小
    image = image.resize((width, height))

    # 将修改后的图片写入内存
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer

@app.route('/image/<path:filename>', methods=['GET'])
def handle_image(filename):
    if filename == None:
        return "NO Resource!"
    # 解析 URL 中的 width 和 height 参数
    width = request.args.get("width", type=int)
    height = request.args.get("height", type=int)


    # 获取原始图片
    try:
        image = get_image("http://192.168.0.114:9000/image/"+filename)
    except RuntimeError as e:
        return f"获取图片失败: {e}"

    # 处理图片大小
    try:
        if height == None:
            height = image.height
        if width == None:
            width = image.width
        print(width, height)
        buffer = handle_image_size(image, width ,height)
    except Exception as e:
        return f"处理图片失败: {e}"

    # 返回修改后的图片
    return send_file(buffer, mimetype="image/jpeg")





if __name__ == '__main__':
    app.run()
