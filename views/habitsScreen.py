import numpy as np
import cv2
import constants
import calendar
import datetime

"""
This screen displays a calendar with the user habits. Blue - brushed once, green - brushed twice, red - no brushing.
Down ⯆ - Return to the home screen
Left ⯇ - Previous calendar month
Right ⯈ - Next calendar month

"""

def Draw(state):
    state.canvas.create_text(constants.LEFT_NAV, text="PREV", anchor="sw", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.RIGHT_NAV, text="NEXT", anchor="se", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.DOWN_NAV, text="HOME", font=constants.FONT, fill="white")
    
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    state.canvas.create_polygon(constants.RIGHT_ARROW, fill="white")
    state.canvas.create_polygon(constants.LEFT_ARROW, fill="white")
        
    today = datetime.date.today()
    display = calendar.Calendar().itermonthdates(today.year, state.selectedMonth)
    
    HEIGHT = 80
    WIDTH = 80
    START = (constants.SCREEN_WIDTH/2 - (WIDTH * 7 / 2), 200)
    OFFSET = 40
    WEEK = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']
    
    row = 0
    col = 0
    
    state.canvas.create_text((constants.SCREEN_WIDTH/2, START[1] - 120), text=calendar.month_name[state.selectedMonth], font=constants.FONT, fill="white")
    for date in display:
        brushingTimes = state.userList[state.selectedUser].brushingTimes
        if date < state.userList[state.selectedUser].registerDate or date > today:
            color = "black"
        else:
            if date in brushingTimes:
                if brushingTimes[date] == 1:
                    color = "blue" # blue
                else:
                    color = "green" # green
            else:
                color = "red" # red
        
        state.canvas.create_rectangle((START[0] + col * WIDTH + 1, START[1] + row * HEIGHT + 1), ((START[0] + (col + 1) * WIDTH, START[1] + (row + 1) * HEIGHT)), fill=color, outline="white")
        state.canvas.create_text((START[0] + col * WIDTH + OFFSET, START[1] + (row + 1) * HEIGHT - OFFSET), text=str(date.day), font=constants.FONT, fill="white")
        if row == 0:
            state.canvas.create_text((START[0] + col * WIDTH + OFFSET, START[1] - OFFSET), text=WEEK[col], font=constants.FONT, fill="white")
    
        col += 1
        
        if col % 7 == 0:
            col = 0
            row += 1   
	
    for id in range(len(state.trailPoints) - 1):
        if id == 0: # earliest - darkest
            color = "#006600"
        elif id == 1:
            color = "#009900"
        elif id == 2:
            color = "#00CC00"
        elif id == 3:
            color = "#00FF00"
        coords = state.trailPoints[id][0], state.trailPoints[id][1], state.trailPoints[id + 1][0], state.trailPoints[id + 1][1]
        state.canvas.create_line(coords, fill=color, width=10.0)
    state.canvas.update()
    state.canvas.delete("all")

