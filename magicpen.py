import cv2 as cv
import numpy as np


Width, Height = 1300, 800

# capture = cv.VideoCapture("http://192.168.1.96:4747/mjpegfeed")
capture = cv.VideoCapture(0)
capture.set(10, 150)
capture.set(3, Width)
capture.set(4, Height)

# pen = (0, 113, 0, 120, 255, 158), (0, 255, 0)
pen = (104, 0, 0, 179, 150, 86), (255, 0, 0)
mode = 'magic'
mode_counter = 200
counter_bool = False
rainbow = [(148, 0, 211), (75, 0, 130), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 127, 0), (255, 0, 0)] # RGB
active_color = pen[1]
opacity = 1
magical = False
canvas = []


colors = {
    'Blue': {
        'color': (255, 0, 0),
        'size': 7,
        'x': 0,
        'y': 10,
        'pos': (0, 10)
    },
    'Red': {
        'color': (0, 0, 255),
        'size': 7,
        'x': 0,
        'y': 180,
        'pos': (0, 180)
    },
    'Green': {
        'color': (0, 255, 0),
        'size': 7,
        'x': 0,
        'y': 350,
        'pos': (0, 350)
    },
    'Yellow': {
        'color': (0, 255, 255),
        'size': 7,
        'x': 0,
        'y': 520,
        'pos': (0, 520)
    }
}

def preprocess_image(frame):
    mask = cv.inRange(frame, pen[0][:3], pen[0][3:])
    mask = cv.dilate(mask, (3, 3), iterations=2)
    mask = cv.erode(mask, (3,3), iterations=1)
    contours, heirarchy = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    
    return contours

def display_options(img):
    w, h = Width // 10, 160
    cv.rectangle(img, (Width - 2*w + 50, Height-h-50), (Width, Height), (255, 255, 0), -1)
    if mode == 'draw':
        for color in colors.keys():
            cv.rectangle(img, (colors[color]['pos']), (colors[color]['x']+w, colors[color]['y']+h), colors[color]['color'], 3)
            cv.putText(img, color, (colors[color]['x']+int(w*0.2), colors[color]['y']+int(h*0.5)), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), thickness = 3)
        
        cv.rectangle(img, (Width - Width // 10, 0), (Width, 100), (150, 150, 150), -1)
        cv.putText(img, 'Clear', (int(Width * 0.91), 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv.putText(img, 'Magic', (Width - 2*w + 100, Height-h+30), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    elif mode == 'magic':
        cv.putText(img, 'Draw', (Width - 2*w + 100, Height-h+30), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

def check_position(c):
    global active_color, mode, magical, opacity, mode_counter, counter_bool

    if counter_bool:
        mode_counter -= 1
        if mode_counter < 0:
            counter_bool = False
            mode_counter = 200

    area = cv.contourArea(c)
    if int(area) in range(150, 3000):
        x, y, w, h = cv.boundingRect(c)
        if mode=='draw':
            if x > int(Width * 0.9) and y < 100:
                print('Canvas cleared')
                canvas.clear()
            elif x > 1090 and y > 590 and not counter_bool: 
                mode = 'magic'
                counter_bool = True
                magical = True
            elif not (x < Width // 10):
                cv.circle(frame, (x+w//2, y), 50, active_color, )
                cv.rectangle(frame, (x, y), (x+w, y+h), active_color, 2)
                canvas.append(((x+w//2, y), active_color))
            else:
                for color in colors.keys():
                    if x in range(colors[color]['x'], colors[color]['x'] + Width // 10) and y in range(colors[color]['y'], colors[color]['y'] + 160):
                            active_color = colors[color]['color']
        elif mode=='magic':
            if not magical:
                opacity = 1
            magical = True
            cv.rectangle(frame, (x, y), (x+w, y+h), active_color, 2)
            if x > 1090 and y > 590 and not counter_bool:
                mode = 'draw'
                counter_bool = True
                magical = False
            for color in rainbow:
                cv.circle(frame, (x+w//2, y), 7, color[::-1], -1)
                canvas.append(((x+w//2, y), color[::-1], 1))
                y += 10

while True:
    success, frame = capture.read()
    overlay = frame.copy()

    contours = preprocess_image(frame)

    for c in contours:
        check_position(c)
            
    for c in canvas:
        cv.circle(overlay, c[0], 10, c[1], -1)
    
    if magical:
        opacity -= 0.02
        if opacity < 0:
            magical = False
            canvas.clear()

    cv.addWeighted(overlay, opacity, frame, 1-opacity, 0, frame)

    display_options(frame)

    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
quit()