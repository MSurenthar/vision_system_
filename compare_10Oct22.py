from skimage.metrics import structural_similarity as compare_ssim
from tkinter import *
from picamera import PiCamera
import imutils,cv2,datetime,sys,time,shutil,tkinter.messagebox,threading
import RPi.GPIO as pin
pin.setmode(pin.BCM)
pin.setwarnings(False)
pin.setup(21,pin.OUT)
pin.setup(20,pin.IN,pull_up_down=pin.PUD_DOWN)

camera=PiCamera() 

win = Tk()

# Set the size of the window
win.geometry("600x400")
win.title("CV System")

running = True
idx = 0

def print_text():
    win.after(1000, print_text)

def on_start():
        global running
        running=True

        camera.resolution=(1000,1000)
        camera.brightness=44
        camera.contrast=40
        #camera.vflip=True
        # img_name1="{}.jpg".format(datetime.datetime.now())
        camera.start_preview()
        time.sleep(2)
        
        camera.stop_preview()
        camera.capture("test.jpeg")
       
        img=cv2.imread("test.jpeg")

        crop= img[300:700,400:775]

        cv2.imwrite("final2.jpeg",crop)

        imageA = cv2.imread("final1.jpeg")
        imageB = cv2.imread("final2.jpeg")

        # convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)


        histogram = cv2.calcHist([grayA], [0],
                                None, [256], [0, 256])


        histogram1 = cv2.calcHist([grayB], [0],
                                None, [256], [0, 256])

    
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        # print("SSIM: {}".format(score))

    
        thresh = cv2.threshold(diff, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contour
        for c in cnts:
            
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)


        c1, c2 = 0, 0
        
        # Euclidean Distance between data1 and test
        i = 0
        while i<len(histogram) and i<len(histogram1):
            c1+=(histogram[i]-histogram1[i])**2
            i+= 1
        c1 = c1**(1 / 2)

        

        if(c1 > 2800):
            # src_path = r"/home/zrai-sgd/Desktop/CV system/test.jpeg"
            src_path = r"test.jpeg"
            img_name2=r"rejected/{}.jpg".format(datetime.datetime.now())
            # dst_path = r"/home/zrai-sgd/Desktop/CV system/rejected/img_name.jpeg"
            shutil.move(src_path, img_name2)
            tkinter.messagebox.showinfo("output","Rejected")
           
            # img_name="/home/zrai-sgd/Desktop/CV system/rejected/{}.jpg".format(datetime.datetime.now())
            # cv2.imwrite(img_name, imageB)

        else:
            src_path = r"test.jpeg"
            img_name3=r"selected/{}.jpg".format(datetime.datetime.now())
            # dst_path = r"/home/zrai-sgd/Desktop/CV system/rejected/img_name.jpeg"
            shutil.move(src_path, img_name3)
            tkinter.messagebox.showinfo("output","Selected")
    
        # if(c1>1000):
        #     print("REJECTED")
        

        # else:
        #     print("SELECTED")
            

        print(c1)    
        
        # show the output images
        # cv2.imshow("Original", imageA)
        cv2.imwrite("diff.jpeg", diff)

def on_stop():
    global running
    running=False
    sys.exit()

def listen_button():
    while True:
        if pin.input(20) :
            print("Button Pressed")
            on_start()
            print("Process Completed")
            time.sleep(2)
        time.sleep(.1)

th=threading.Thread(target=listen_button,daemon=True)
th.start()
canvas = Canvas(win, bg="skyblue3", width=600, height=60)
canvas.create_text(300, 25, text="Vision System", font=('', 13))
canvas.pack()

# Add a Button to start/stop the loop
# capture= ttk.Button(win,text="Capture", command=on_cap)
# capture.pack(padx=100)

Button(win, text="Start",height=5 ,width=20, command=on_start).pack()

Button(win, text="Stop",height=5 ,width=20, command=on_stop).pack()
# stop = ttk.Button(win, text="Stop", command=on_stop)
# stop.pack(padx=10)

# Run a function to print text in window
win.after(1000, print_text)


win.mainloop()