from PIL import Image

def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    w,h = img.size
    for i in range(w):
        for j in range(h):
            r,g,b = img.getpixel((i,j))
            if r != g != b: return False
    return True

def main():
    is_grey_scale(./static/Images/NormalChest1.jpeg)




if __name__ == '__main__':
    main()