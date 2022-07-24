from window_capture import WindowCapture
import cv2 as cv
import pyautogui
from time import sleep

# set game resolution to 640x480
# crop image
# crop_img = img[y:y+h, x:x+w]


cap = WindowCapture('Timberman')

game_frame = cap.get_screenshot()
game_height, game_width, _ = game_frame.shape

# play button reference
p_but_cord = (game_width//2, game_height-35)
p_but_size = (100, 60)
p_but_color = [42, 33, 157]

p_but_min = (p_but_cord[0] - (p_but_size[0] // 2), p_but_cord[1] - (p_but_size[1] // 2))
p_but_max = (p_but_cord[0] + (p_but_size[0] // 2), p_but_cord[1] + (p_but_size[1] // 2))



# detection lef cord
d_l_cord = ((game_width//2)-80, (game_height//2)+28)
d_l_min = (d_l_cord[0] - 5 , d_l_cord[1] -25 - 3)
d_l_max = (d_l_cord[0] + 5, d_l_cord[1] + 3)

# detection right cord
d_r_cord = ((game_width//2)+80, (game_height//2)+28)
d_r_min = (d_r_cord[0] - 5, d_r_cord[1] -25 - 3)
d_r_max = (d_r_cord[0] + 5, d_r_cord[1] + 3)



template_left = []
template_right = []

# states
game_on = False
left = True

l_found = 0
r_found = 0

pyautogui.click(200, 200)
while True:
    game_frame = cap.get_screenshot()

    # check if has play button on screen
    play_button = game_frame[p_but_cord[1]:p_but_cord[1]+1, p_but_cord[0]-1:p_but_cord[0]+1]
    if play_button[0][0][0] == p_but_color[0] and play_button[0][0][1] == p_but_color[1] and play_button[0][0][2] == p_but_color[2]:
        game_on = False
    else:
        if not game_on:
            left = True
            game_on = True
            sleep(2)
            game_frame = cap.get_screenshot()
            # set left an right template
            template_left = game_frame[d_l_cord[1]-25:d_l_cord[1], d_l_cord[0]:d_l_cord[0]+1]
            template_right = game_frame[d_r_cord[1]-25:d_r_cord[1], d_r_cord[0]:d_r_cord[0]+1]


    if game_on:
        if left:
            new_template = game_frame[d_l_cord[1]-25:d_l_cord[1], d_l_cord[0]:d_l_cord[0]+1]
            for i in range(25, 0, -1):
                pixel = new_template[i-1:i, 0:1][0][0][0]
                template_pixel = template_left[i-1:i, 0:1][0][0][0]

                if not pixel == template_pixel:
                    left = False
                    break
            pyautogui.press('a')

        else:
            new_template = game_frame[d_r_cord[1]-25:d_r_cord[1], d_r_cord[0]:d_r_cord[0]+1]
            for i in range(25, 0, -1):
                pixel = new_template[i-1:i, 0:1][0][0][0]
                template_pixel = template_right[i-1:i, 0:1][0][0][0]

                if not pixel == template_pixel:
                    left = True
                    break
            pyautogui.press('d')

    # draw for debug
    if game_on:
        # play button
        cv.rectangle(game_frame, p_but_min, p_but_max, (0, 0, 255), 3)

        if left:
            #left, right
            cv.rectangle(game_frame, d_l_min, d_l_max, (0, 255, 0), 3)
            cv.rectangle(game_frame, d_r_min, d_r_max, (0, 0, 255), 3)
        else:
            cv.rectangle(game_frame, d_l_min, d_l_max, (0, 0, 255), 3)
            cv.rectangle(game_frame, d_r_min, d_r_max, (0, 255, 0), 3)


    else:
        # play button
        cv.rectangle(game_frame, p_but_min, p_but_max, (0, 255, 0), 3)

    # show
    cv.imshow('frame', game_frame)
    cv.waitKey(1)