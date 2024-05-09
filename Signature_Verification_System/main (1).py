import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match

# Match Threshold
THRESHOLD = 85
FORGERY_THRESHOLD = 30  # Adjust as needed

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("Image files", "*.jpeg;*.png;*.jpg"),
    ])
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("Capture Signature")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Capture Signature", frame)

        k = cv2.waitKey(1)
        if k == 27:  # ESC pressed
            print("Escape hit, closing...")
            break
        elif k == 32:  # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            if sign == 1:
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))

    cam.release()
    cv2.destroyAllWindows()
    return True

def capture_image(ent, sign=1):
    if sign == 1:
        filename = os.path.join(os.getcwd(), 'temp', 'test_img1.png')
    else:
        filename = os.path.join(os.getcwd(), 'temp', 'test_img2.png')

    res = messagebox.askquestion(
        'Capture Signature', 'Press Space Bar to capture signature and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def check_similarity(window, path1, path2):
    if not (os.path.exists(path1) and os.path.exists(path2)):
        messagebox.showerror("Error", "Invalid file paths!")
        return False

    result = match(path1=path1, path2=path2)
    if result is not None:
        error_percentage = 100 - result
        if error_percentage < FORGERY_THRESHOLD:
            messagebox.showinfo("Similar Signatures",
                                f"The signatures are similar. The percentage of difference is {error_percentage:.2f}%, "
                                f"which is not significant enough to indicate forgery.")
        elif result <= THRESHOLD:
            messagebox.showerror("Failure: Signatures Do Not Match",
                                 f"Signatures are {error_percentage:.2f}% different. This may indicate a forgery.")
        else:
            messagebox.showinfo("Success: Signatures Match",
                                f"Signatures are {result:.2f}% similar.")
    else:
        messagebox.showerror("Error", "Signature comparison failed!")
    return True

root = tk.Tk()
root.title("Signature Verification System - Misr University of Science and Technology")
root.geometry("600x400")
root.configure(bg='#F4ECF7')

compare_label = tk.Label(root, text="Compare Two Signatures:", font=("Arial", 16, "bold"), bg='#F4ECF7')
compare_label.place(x=150, y=20)

img1_message = tk.Label(root, text="Signature 1:", font=("Arial", 14), bg='#F4ECF7')
img1_message.place(x=50, y=80)

image1_path_entry = tk.Entry(root, font=("Arial", 14), width=30)
image1_path_entry.place(x=180, y=80)

img1_capture_button = tk.Button(
    root, text="Capture", font=("Arial", 12), bg='#7FB3D5', fg='white', padx=10,
    command=lambda: capture_image(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=470, y=80)

img1_browse_button = tk.Button(
    root, text="Browse", font=("Arial", 12), bg='#7FB3D5', fg='white', padx=10,
    command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=470, y=120)

img2_message = tk.Label(root, text="Signature 2:", font=("Arial", 14), bg='#F4ECF7')
img2_message.place(x=50, y=170)

image2_path_entry = tk.Entry(root, font=("Arial", 14), width=30)
image2_path_entry.place(x=180, y=170)

img2_capture_button = tk.Button(
    root, text="Capture", font=("Arial", 12), bg='#7FB3D5', fg='white', padx=10,
    command=lambda: capture_image(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=470, y=170)

img2_browse_button = tk.Button(
    root, text="Browse", font=("Arial", 12), bg='#7FB3D5', fg='white', padx=10,
    command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=470, y=210)

compare_button = tk.Button(
    root, text="Compare", font=("Arial", 14), bg='#4CAF50', fg='white', padx=10,
    command=lambda: check_similarity(window=root,
                                      path1=image1_path_entry.get(),
                                      path2=image2_path_entry.get()))
compare_button.place(x=250, y=290)

root.mainloop()