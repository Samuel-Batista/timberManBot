from window_capture import WindowCapture
import cv2 as cv
import math

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
d_l_cord = ((game_width//2)-90, (game_height//2)+40)
d_l_min = (d_l_cord[0] - 5 , d_l_cord[1] -25 - 3)
d_l_max = (d_l_cord[0] + 5, d_l_cord[1] + 3)

# detection right cord
d_r_cord = ((game_width//2)+90, (game_height//2)+40)
d_r_min = (d_r_cord[0] - 5, d_r_cord[1] -25 - 3)
d_r_max = (d_r_cord[0] + 5, d_r_cord[1] + 3)


template_left = []
template_right = []

# states
game_on = False
left = True

l_found = 0
r_found = 0


while True: 
    game_frame = cap.get_screenshot()

    # check if has play button on screen
    play_button = game_frame[p_but_cord[1]:p_but_cord[1]+1, p_but_cord[0]-1:p_but_cord[0]+1]
    if play_button[0][0][0] == p_but_color[0] and play_button[0][0][1] == p_but_color[1] and play_button[0][0][2] == p_but_color[2]:
        game_on = False
    else:
        if not game_on:
            game_on = True
            left = True


    if game_on:
        # reset left and right to prevent bugs
        l_found = 0
        r_found = 0

        
        # find left black pixel
        for h in range(d_l_cord[1], 0, -1):
            b, g, r = game_frame[h-1:h, d_l_cord[0]-1:d_l_cord[0]][0][0]
            if b < 25 and g < 25 and r < 25:
                l_found = h
                break
        # logic
        distance = d_l_cord[1] - l_found
        steps = math.floor((distance / 65) + 0.5)
        
        # action
        if steps == 0:
            left = False
        
        
        for h2 in range(d_r_cord[1], 0, -1):
            b, g, r = game_frame[h2-1:h2, d_r_cord[0]-1:d_r_cord[0]][0][0]
            if b < 25 and g < 25 and r < 25:
                r_found = h2
                break

        # logic
        distance = d_r_cord[1] - r_found
        steps = math.floor((distance / 65) + 0.5)
        
        # action
        if steps == 0:
            left = True


    # draw for debug
    if game_on:
        if left:
            # left and right lines
            cv.line(game_frame, (d_l_cord[0], l_found), (d_l_cord[0], d_l_cord[1]), (0, 255, 0), 10)
            cv.line(game_frame, (d_r_cord[0], r_found), (d_r_cord[0], d_r_cord[1]), (0, 0, 255), 50)

            # for line in range(d_l_cord[1], 0, -65):
            #     cv.line(game_frame, (d_l_cord[0]-100, line), (d_l_cord[0]-50, line), (0, 255, 0), 2)

        else:
            # left and right lines
            cv.line(game_frame, (d_l_cord[0], l_found), (d_l_cord[0], d_l_cord[1]), (0, 0, 255), 50)
            cv.line(game_frame, (d_r_cord[0], r_found), (d_r_cord[0], d_r_cord[1]), (0, 255, 0), 10)

    # show
    cv.imshow('frame', game_frame)
    cv.waitKey(1)