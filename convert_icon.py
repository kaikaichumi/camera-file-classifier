from PIL import Image

# 打开 PNG 图片（已有透明背景）
img = Image.open('icon.png')

# 确保是 RGBA 模式
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# 调整大小为常见的图标尺寸（256x256）
img = img.resize((256, 256), Image.Resampling.LANCZOS)

# 保存为 ICO 格式
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

print("Icon converted successfully from PNG to ICO: icon.ico")
