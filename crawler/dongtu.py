import sys
import imageio as gio
import cv2

st = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def test(f):
    pics = gio.mimread(f)
    A = []
    for i in pics:
        u, v, _ = i.shape
        c = i * 0 + 255
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        for j in range(0, u, 6):
            for k in range(0, v, 6):
                pix = gray[j, k]
                b, g, r, _ = i[j, k]
                zifu = st[int(((len(st) - 1) * pix) / 256)]
                cv2.putText(c, zifu, (k, j),
                            cv2.FONT_HERSHEY_COMPLEX, 0.3,
                            (int(b), int(g), int(r)), 1)
        A.append(c)

        gio.mimsave('out.gif', A, 'gif', duration=0.1)


if __name__ == "__main__":
    filename = sys.argv[1]
    test(filename)