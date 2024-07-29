import PIL
import platform


print(platform.python_version())
print(PIL.__file__)
print(PIL.__version__)

from PIL import Image
print(Image.__file__)
