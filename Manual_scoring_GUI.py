import cv2 as cv
import pandas as pd
import os
import PySimpleGUI as sg
from tabulate import tabulate
import sys
import numpy as np

inputs = {}

# Choose the import location, export location and setup.
default = {}
default["Import location"] = r"C:\Users\hazza\Desktop\Video.mp4"
default["Export location"] = r"C:\Users\hazza\Desktop"
default["Num"]             = 4
sg.theme("DarkTeal2")
layout  = []
layout += [[sg.T("")], [sg.Text("Choose the location of the video to score",size=(29,1)), 
            sg.Input(key="Import" ,enable_events=True,default_text=default["Import location"]),
            sg.FileBrowse(key="Import2")]]
layout += [[sg.T("")], [sg.Text("Choose a folder for the export location",size=(29,1)),
            sg.Input(key="Export" ,enable_events=True,default_text=default["Export location"]),
            sg.FolderBrowse(key="Export2")]]
layout += [[sg.T("")],[sg.Text("Choose how many events you want to score"), 
            sg.Combo(list(range(1,15+1)),key="Num",enable_events=True,default_value=default["Num"])]]
layout += [[sg.T("")], [sg.Button("Submit")]]
window  = sg.Window('Manual scoring GUI', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        window.close()
        sys.exit()
    elif event == "Submit":
        inputs['Import location'] = values["Import"]
        inputs['Export location'] = values["Export"]
        inputs['Num events']      = values["Num"]
        window.close()
        break
    
# Use the existing settings, if there is a csv file called "Manual_scoring_settings"
# in the same place as the video import folder.
video_folder_path  = os.path.dirname(inputs['Import location'])
settings_file_path = os.path.join(video_folder_path, "Manual_scoring_settings.csv")

default = {}
default['Settings'] = 'True'
sg.theme("DarkTeal2")
layout  = []
layout += [[sg.T("")],[sg.Text("Use scoring settings defined previously?"), 
            sg.Combo(['True','False'],key="Settings",
            enable_events=True,default_value=default['Settings'])]]
layout += [[sg.T("")],[sg.Button("Submit")]]
window  = sg.Window('Manual scoring GUI', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        window.close()
        sys.exit()
    elif event == "Submit":
        inputs["Settings"] = (True if values['Settings']=='True' else False)
        window.close()
        break

event_types = ['Point event','Mutually exclusive','Start-stop event']
event_keys  = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z']

if inputs['Settings'] == True:

    if os.path.isfile(settings_file_path) == False:
        print('Make sure the "Manual_scoring_settings.csv" file is located in '+
              'the same folder as the import video file.')
        print('These are automatically created in this location after defining '+
              'new settings.')
        sys.exit()
    
    df = pd.read_csv(settings_file_path)
    inputs['Event names'] = list(df['Event names'].astype(str))
    inputs['Event types'] = list(df['Event types'].astype(str))
    inputs['Event keys']  = list(df['Event keys' ].astype(str))
    
    # Check whether a key was entered that was not allowed.
    for key in inputs['Event keys']:
        if key not in event_keys:
            print(key+' is not allowed as an event key. Only letters of the '+
                  'alphabet should be in the "Manual_scoring_settings.csv" file.')
            sys.exit()
            
    # Check whether the event types are only within 'Point event', 'Mutually 
    # exclusive' and 'Start-stop event'.
    for type1 in inputs['Event types']:
        if type1 not in event_types:
            print(type1+' is not allowed as an event type. Only "Point event", '+
                  '"Mutually exclusive" and "Start-stop event" are allowed in '+
                  'the "Manual_scoring_settings.csv" file.')
            sys.exit()
            
    # Check whether some event keys and names are the same.
    if len(set(inputs['Event names'])) != len(inputs['Event names']):
        print('Make the event names have no duplicates.')
        sys.exit()
    if len(set(inputs['Event keys'])) != len(inputs['Event keys']):
        print('Make the event keys have no duplicates.')
        sys.exit()
            
    print('Use the space bar to pause and the left and right arrow keys to move one frame at a time.')
    print('Use the keys below to score events and press backspace to delete the last scored event.\n')
    headings = ['Event types', 'Event keys', 'Event names']
    table    = [inputs[heading] for heading in headings]
    table    = list(np.array(table).T)
    print(tabulate(table, headers=headings))
    print('')

elif inputs['Settings'] == False:
    
    # Choose the import location, export location and setup.
    default = {}
    default["Event type"] = 'Point event'
    sg.theme("DarkTeal2")
    layout  = [[sg.T("")], [sg.Text("Choose the event types, keys for scoring and the event names")], [sg.T("")], 
               [sg.Text("Types",size=(15,1)), sg.Text("Keys",size=(4,1)), sg.Text("Names",size=(20,1))]]
    for i in range(1,inputs['Num events']+1):
        layout += [
                   [sg.Combo(event_types,
                             key="Event_type"+str(i),enable_events=True,default_value=default["Event type"],size=(15,1)),
                    sg.Combo(event_keys,key="Event_key"+str(i),enable_events=True,default_value=event_keys[i-1],size=(3,1)),
                    sg.Input(key="Event_name"+str(i),enable_events=True,default_text='Event name '+str(i),size=(20,1))]]
    layout += [[sg.T("")], [sg.Button("Submit")]]
    window  = sg.Window('Manual scoring GUI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            inputs['Event names'] = []
            inputs['Event types'] = []
            inputs['Event keys'] = []
            for i in range(1,inputs['Num events']+1):
                inputs['Event names'] += [values['Event_name'+str(i)]]
                inputs['Event types'] += [values['Event_type'+str(i)]]
                inputs['Event keys']  += [values['Event_key' +str(i)]]
            window.close()
            break
        
    # Check whether some event keys and names are the same.
    if len(set(inputs['Event names'])) != len(inputs['Event names']):
        print('Make the event names have no duplicates.')
        sys.exit()
    if len(set(inputs['Event keys'])) != len(inputs['Event keys']):
        print('Make the event keys have no duplicates.')
        sys.exit()

    print('Use the space bar to pause and the left and right arrow keys to move one frame at a time.')
    print('Use the keys below to score events and press backspace to delete the last scored event.\n')
    headings = ['Event types', 'Event keys', 'Event names']
    table    = [inputs[heading] for heading in headings]
    table    = list(np.array(table).T)
    print(tabulate(table, headers=headings))
    print('')
    
    # Export the manual scoring settings.
    df = pd.DataFrame(table, columns=headings)
    export_settings_path = os.path.join(
        os.path.dirname(inputs['Import location']), 'Manual_scoring_settings.csv')
    df.to_csv(export_settings_path, index=False)
    
# Add the computer definitions for each key press.
inputs['Event codes'] = [ord(letter) for letter in inputs['Event keys']]
outputs = {inputs['Event names'][i]:[] for i in range(len(inputs['Event names']))}
    
import_name = os.path.basename(inputs['Import location'])
import_location = os.path.dirname(inputs['Import location'])
import_destination = inputs['Import location']
export_name = 'Timestamps.xlsx'
export_location = inputs['Export location']
export_destination = os.path.join(export_location, export_name)
window = 'Video'
warning = "!!! Failed cap.read()"
cap = cv.VideoCapture(import_destination)
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv.CAP_PROP_FPS)
previous_me = 'No_previous_mutually_exclusive_timestamp'
list_frames = []

def set_frame(x):
    cap.set(cv.CAP_PROP_POS_FRAMES, x)
def setSpeed(val):
    global playSpeed
    playSpeed = max(val,1)
playSpeed = 10
cv.namedWindow(window)
trackbar = 'Time'
cv.createTrackbar(trackbar, window, 0, frame_count, set_frame)
cv.createTrackbar('Speed', window, playSpeed, 100, setSpeed)

while cap.isOpened():
    
    # Update the picture of the mouse.
    ret, frame = cap.read()
    if ret == False:
        print(warning)
        break
    cv.imshow(window,frame)
    # Set the speed of the video.
    k = cv.waitKeyEx(playSpeed)
    
    # If an event key is pressed, add the frame number to the outputs dictionary.
    if k in inputs['Event codes']:
        frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        frame_no -= 1
        ind = inputs['Event codes'].index(k)
        cv.setTrackbarPos(trackbar, window, frame_no)
        num_frames = str(sum([len(outputs[key]) for key in outputs.keys()]))
        frame_no   = str(frame_no)
        event_name = inputs['Event names'][ind]
        if inputs['Event types'][ind] == 'Point event':
            outputs[event_name] += [int(frame_no)]
            print(f'({num_frames}) Saved frame {frame_no} for {event_name}.')
        elif inputs['Event types'][ind] == 'Mutually exclusive':
            if previous_me == 'No_previous_mutually_exclusive_timestamp':
                outputs[event_name]  += [int(frame_no)]
            if previous_me != 'No_previous_mutually_exclusive_timestamp' and previous_me != event_name:
                outputs[event_name]  += [int(frame_no)]
                outputs[previous_me] += [int(frame_no)]
            previous_me = event_name
            print(f'({num_frames}) Saved frame {frame_no} for {event_name}.')
        elif inputs['Event types'][ind] == 'Start-stop event':
            outputs[event_name] += [int(frame_no)]
            num_frames_ind = len(outputs[event_name])
            start_or_stop = ('Stop' if num_frames_ind % 2 == 0 else 'Start') 
            print(f'({num_frames}) Saved frame {frame_no} for {event_name} ({start_or_stop}).')
        
    # If backspace is pressed, delete the last frame from list_frames.
    if k == 8:
        if len(list_frames) > 0:
            print('# Deleted frame '+str(list_frames[-1])) 
            list_frames = list_frames[:-1]
        else:
            print('# There are no more frames to delete')
        frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        frame_no -= 1
        cv.setTrackbarPos(trackbar, window, frame_no)
    
    # # If r is pressed, rewind 10 seconds.
    # if k == ord('r'):
    #     frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
    #     frame_no -= 1
    #     rewi_frame = (frame_no-10*30 if frame_no>10*30 else 0)
    #     cv.setTrackbarPos(trackbar, window, rewi_frame)
    
    # If the left arrow key is pressed, go back 1 frame.
    if k == 2424832:
        frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        frame_no -= 1
        prev_frame = (frame_no-1 if frame_no>0 else 0)
        cv.setTrackbarPos(trackbar, window, prev_frame)
        
    # If the right arrow key is pressed, go forward 1 frame.
    if k == 2555904:
        frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        frame_no -= 1
        next_frame = (frame_no+1 if frame_no<frame_count else frame_count)
        cv.setTrackbarPos(trackbar, window, next_frame)
    
    # If space is pressed, pause the video.
    if k == 32:
        
        frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        frame_no -= 1
        cv.setTrackbarPos(trackbar, window, frame_no)
        # Update the picture of the mouse.
        ret, frame = cap.read()
        if ret == False:
            print(warning)
            break
        cv.imshow(window,frame)
        
        while cap.isOpened():
        
            k = cv.waitKeyEx(0)
            
            # If space is pressed again, play the video.
            if k == 32:
                break
            
            # While the video is paused, allow the other buttons to be pressed.
            
            # If the red X button is pressed, close the window.
            if cv.getWindowProperty(window,cv.WND_PROP_VISIBLE) < 1:
                break
            
            # If an event key is pressed, add the frame number to the outputs dictionary.
            if k in inputs['Event codes']:
                frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
                frame_no -= 1
                ind = inputs['Event codes'].index(k)
                cv.setTrackbarPos(trackbar, window, frame_no)
                num_frames = str(sum([len(outputs[key]) for key in outputs.keys()]))
                frame_no   = str(frame_no)
                event_name = inputs['Event names'][ind]
                if inputs['Event types'][ind] == 'Point event':
                    outputs[event_name] += [int(frame_no)]
                    print(f'({num_frames}) Saved frame {frame_no} for {event_name}.')
                elif inputs['Event types'][ind] == 'Mutually exclusive':
                    if previous_me == 'No_previous_mutually_exclusive_timestamp':
                        outputs[event_name]  += [int(frame_no)]
                    if previous_me != 'No_previous_mutually_exclusive_timestamp' and previous_me != event_name:
                        outputs[event_name]  += [int(frame_no)]
                        outputs[previous_me] += [int(frame_no)]
                    previous_me = event_name
                    print(f'({num_frames}) Saved frame {frame_no} for {event_name}.')
                elif inputs['Event types'][ind] == 'Start-stop event':
                    outputs[event_name] += [int(frame_no)]
                    num_frames_ind = len(outputs[event_name])
                    start_or_stop = ('Stop' if num_frames_ind % 2 == 0 else 'Start') 
                    print(f'({num_frames}) Saved frame {frame_no} for {event_name} ({start_or_stop}).')
                
            # If backspace is pressed, delete the last frame from list_frames.
            if k == 8:
                if len(list_frames) > 0:
                    print('# Deleted frame '+str(list_frames[-1])) 
                    list_frames = list_frames[:-1]
                else:
                    print('# There are no more frames to delete')
                
            # # If r is pressed, rewind 10 seconds.
            # if k == ord('r'):
            #     frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
            #     frame_no -= 1
            #     rewi_frame = (frame_no-10*30 if frame_no>10*30 else 0)
            #     cv.setTrackbarPos(trackbar, window, rewi_frame)
            #     # Update the picture of the mouse.
            #     ret, frame = cap.read()
            #     if ret == False:
            #         print(warning)
            #         break
            #     cv.imshow(window,frame)
                
            # If the left arrow key is pressed, go back 1 frame.
            if k == 2424832:
                frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
                frame_no -= 1
                prev_frame = (frame_no-1 if frame_no>0 else 0)
                cv.setTrackbarPos(trackbar, window, prev_frame)
                # Update the picture of the mouse.
                ret, frame = cap.read()
                if ret == False:
                    print(warning)
                    break
                cv.imshow(window,frame)
                
            # If the right arrow key is pressed, go forward 1 frame.
            if k == 2555904:
                frame_no = int(cap.get(cv.CAP_PROP_POS_FRAMES))
                frame_no -= 1
                next_frame = (frame_no+1 if frame_no<frame_count else frame_count)
                cv.setTrackbarPos(trackbar, window, next_frame)
                # Update the picture of the mouse.
                ret, frame = cap.read()
                if ret == False:
                    print(warning)
                    break
                cv.imshow(window,frame)
                
    # If the red X button is pressed, close the window.
    if cv.getWindowProperty(window,cv.WND_PROP_VISIBLE) < 1:
        break
  
cap.release()
cv.destroyAllWindows()

num_frames = sum([len(outputs[key]) for key in outputs.keys()])

if num_frames > 0:
    
    # Create an excel file with the timestamps from 0 frames until the end of the video.
    df = pd.DataFrame()
    df['Time (frames)'] = range(frame_count)
    df['Time (secs)']   = df['Time (frames)'] * fps
    df['Time (ms)']     = df['Time (frames)'] * fps * 1000
    def binary_timestamps(time, frames):
        if time in frames:
            return(1)
        else:
            return(0)
    for ind in range(len(inputs['Event names'])):
        event_name = inputs['Event names'][ind]
        event_type = inputs['Event types'][ind]
        if event_type == 'Point event':
            df[event_name] = df['Time (frames)'].apply(binary_timestamps, frames=outputs[event_name])
        elif event_type == 'Start-stop event':
            # If the number of timestamps is odd, there is a start but not a
            # corresponding stop at the end.
            if len(outputs[event_name]) % 2 == 1:
                outputs[event_name] += [frame_count]
            all_events = []
            for i in range(1,len(outputs[event_name])):
                all_events += list(range(int(outputs[event_name][i-1]), int(outputs[event_name][i])+1))
            df[event_name] = df['Time (frames)'].apply(binary_timestamps, frames=all_events)
        elif event_type == 'Mutually exclusive':
            # If the number of timestamps is odd, there is a start but not a
            # corresponding stop at the end.
            if len(outputs[event_name]) % 2 == 1:
                outputs[event_name] += [frame_count]
            all_events = []
            for i in range(1,len(outputs[event_name])):
                all_events += list(range(int(outputs[event_name][i-1]), int(outputs[event_name][i])))
            df[event_name] = df['Time (frames)'].apply(binary_timestamps, frames=all_events)
    df.to_excel(os.path.join(export_location, 'Binary_timestamps.xlsx'), index=False)
        
    # Remove duplicates and sort the frame numbers from earliest to latest.
    for key in outputs.keys():
        outputs[key] = sorted(set(outputs[key]))
    
    # Add nans to make each list the same length.
    max_len = max([len(outputs[key]) for key in outputs.keys()])
    for key in outputs.keys():
        cur_len = len(outputs[key])
        outputs[key] = outputs[key] + (max_len-cur_len)*[np.nan]
    
    # Add columns in units of seconds and milliseconds.
    outputs_frames = pd.DataFrame(outputs)
    outputs_secs   = outputs_frames * fps
    outputs_ms     = outputs_frames * fps * 1000
    outputs_frames.columns = [col+' (frames)' for col in outputs_frames.columns]
    outputs_secs.columns   = [col+' (secs)'   for col in outputs_secs.columns]
    outputs_ms.columns     = [col+' (ms)'     for col in outputs_ms.columns]
    
    # Export the data.
    with pd.ExcelWriter(export_destination) as writer:
        outputs_frames.to_excel(writer, sheet_name='Frames', index=False)
        outputs_secs.to_excel(writer, sheet_name='Seconds', index=False)
        outputs_ms.to_excel(writer, sheet_name='Milliseconds', index=False)

    # Export the data as a CSV file.
    # df = pd.DataFrame()
    # df['Number of events']        = list(range(1,len(list_frames)+1))
    # df['Event times (in frames)'] = list_frames
    # df['Event times (in secs)']   = df['Event times (in frames)'] * fps
    # df['Event times (in ms)']     = df['Event times (in frames)'] * fps * 1000
    # outputs.to_csv(export_destination, index=False)
    print('Saved data to csv at '+export_location)
