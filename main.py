import numpy, cv2, sys, datetime
from os import get_terminal_size as terminalsize
from os import rename as renamefile
from os import remove as deletefile
from os import mkdir as createfolder
from random import randint as rand
from subprocess import call as callcommand
from time import sleep as wait
from moviepy.editor import VideoFileClip

try: createfolder("output")
except: pass
try: createfolder("wd")
except: pass

def debug(inp):
    global debugon
    if debugon: print(inp)

def clear():
    for i in range(terminalsize().lines): print("\n")

# set default arguments
res = [1920,1080] # resolution (w,h)
fps = 60 # fps
duration = 120 # duration (seconds)

loop = 1

run = True
argsp = True
debugon = False

try: args = sys.argv[1:]
except: argsp = False

if argsp:
    for arg in args:
        arg = arg.split("=",1)
        has_data = False
        if len(arg) == 2: 
            if len(arg[1]) > 0: has_data = True
        if arg[0] == "-v":
            print("Debug on")
            print(args)
            debugon = True
        elif not has_data:
            print("Missing argument data: argument",arg[0])
            sys.exit()
        else:
            try:
                arg[1] = int(arg[1])
            except:
                print("Incorrect data type in argument (expeceted integar):",arg[0]+"="+arg[1])
                sys.exit()
            if   arg[0] == "-w": res[0]   = arg[1]
            elif arg[0] == "-h": res[1]   = arg[1]
            elif arg[0] == "-f": fps      = arg[1]
            elif arg[0] == "-d": duration = arg[1]
            elif arg[0] == "-l": loop     = arg[1]
            else:
                print("Unknown argument:",arg[0])
                sys.exit()

clear()
print("Resolution: " + str(res[0])+"x"+str(res[1]))
print("FPS: "        + str(fps)                   )
print("Duration: "   + str(duration)+" seconds"   )
if loop != 1: print("Videos: "+str(loop))

cont = input("\nContinue with these vaules? (Y/n): ")
if cont.lower() != "y": 
    print("Exiting program...")
    sys.exit()

print("\nGenerating video. This process can take a long time.")

image_path_base = 'assets/dvdlogo-0'
moving_image = []
for i in range(1,9):
    moving_image.append(cv2.imread(image_path_base+str(i)+".png"))
moving_image_height, moving_image_width = moving_image[0].shape[:2]

total_frames = fps * duration

for il in range(0,loop):
    x_pos = rand(0,res[0]-moving_image_width)
    y_pos = rand(0,res[1]-moving_image_height)
    if rand(1,2) == 1: x_velocity = 5 
    else: x_velocity = -5
    if rand(1,2) == 1: y_velocity = 3
    else: y_velocity = -3

    image = rand(0,7)

    out = cv2.VideoWriter('wd/output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (res[0], res[1]))

    def overlay_image(background, image, x, y):
        img_height, img_width = image.shape[:2]
        roi = background[y:y+img_height, x:x+img_width]
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img_fg = cv2.bitwise_and(image, image, mask=mask)
        dst = cv2.add(background_bg, img_fg)
        background[y:y+img_height, x:x+img_width] = dst

    for frame_idx in range(total_frames):
        bg = numpy.full((res[1], res[0], 3), (0, 0, 0), dtype=numpy.uint8)

        x_pos += x_velocity
        y_pos += y_velocity

        if x_pos <= 0:
            x_pos = 0
            x_velocity = -x_velocity
            colourselected = False
            while not colourselected:
                imagetmp = rand(0,7)
                if image != imagetmp:
                    image = imagetmp
                    colourselected = True
            debug("Bouncing (left)")
        elif x_pos + moving_image_width >= res[0]:
            x_pos = res[0] - moving_image_width
            x_velocity = -x_velocity
            colourselected = False
            while not colourselected:
                imagetmp = rand(0,7)
                if image != imagetmp:
                    image = imagetmp
                    colourselected = True
            debug("Bouncing (right)")
        if y_pos <= 0:
            y_pos = 0
            y_velocity = -y_velocity
            colourselected = False
            while not colourselected:
                imagetmp = rand(0,7)
                if image != imagetmp:
                    image = imagetmp
                    colourselected = True
            debug("Bouncing (top)")
        elif y_pos + moving_image_height >= res[1]:
            y_pos = res[1] - moving_image_height
            y_velocity = -y_velocity
            colourselected = False
            while not colourselected:
                imagetmp = rand(0,7)
                if image != imagetmp:
                    image = imagetmp
                    colourselected = True
            debug("Bouncing (bottom)")

        overlay_image(bg, moving_image[image], x_pos, y_pos)
        out.write(bg)

    out.release()
    cv2.destroyAllWindows()

    print("\nVideo created successfully!")
    print("Converting .avi to .mov...")

    VideoFileClip('wd/output_video.avi').write_videofile('wd/output_video.mov', codec='libx264')
    deletefile('wd/output_video.avi')

    print("Video successfully converted")
    if loop == 1: 
        cont = input("\nWould you like to replace a screensaver now? (Y/n): ")

        if cont.lower() != "y":
            renamefile('wd/output_video.mov',"output/"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%m-%s")+".mov")
            print("Exiting now.")
            print("Reference README.MD for instructions to manually copy the screensaver.")
            sys.exit()
        valid = False
        optionsshort_14 = [
            ["London from Above", "A5AAFF5D-8887-42BB-8AFD-867EF557ED85"],
            ["California's Carrizo Plain", "4A3590EC-FF30-41E7-85FE-210FF6112917"],
            ["Red Sea Coral from Above", "82175C1F-153C-4EC8-AE37-2860EA828004"]
        ]
        options_14 = [
            [0, "Sonoma Evening", "94DAB450-A650-4DFC-99B2-A0F0D8AD6649"],
            [0, "California's Carrizo Plain", "4A3590EC-FF30-41E7-85FE-210FF6112917"],
            [1, "London from Above", "A5AAFF5D-8887-42BB-8AFD-867EF557ED85"],
            [2, "Red Sea Coral from Above", "82175C1F-153C-4EC8-AE37-2860EA828004"]
        ]

        optionscategories_14 = ["Landscapes","Cityscapes","Underwater","Earth"]

        showall = False
        retry = True
        while retry:
            clear()
            while not valid:
                print("\nSelect the screensaver you'd like to replace")

                if not showall:
                    print("  0. Show all")
                    for i in range(0,len(optionsshort_14)):
                        print("  "+str(i+1)+": "+optionsshort_14[i][0])
                    opt = input("\nEnter your selection (0-"+str(len(optionsshort_14))+"): ")
                    try:
                        opt = int(opt)
                        debug(str(opt))
                        if 0 <= opt and opt <= len(optionsshort_14): valid = True
                        else: 
                            clear()
                            print("Invalid choice - enter a number between 0 and "+str(len(optionsshort_14))+" (inclusive)")
                    except:
                        clear()
                        print("Invalid choice - enter a number between 0 and "+str(len(optionsshort_14))+" (inclusive)")

                else:
                    for i in range(0,len(options_14)):
                        print("  "+str(i+1)+": "+optionscategories_14[options_14[i][0]]+" - "+options_14[i][1])
                    print("  0. Return to short list")
                    opt = input("\nEnter your selection (0-"+str(len(options_14))+"): ")
                    try:
                        opt = int(opt)
                        if 0 <= opt and opt <= len(options_14): valid = True
                        else: 
                            clear()
                            print("Invalid choice - enter a number between 0 and "+str(len(options_14))+" (inclusive)")
                    except:
                        clear()
                        print("Invalid choice - enter a number between 0 and "+str(len(options_14))+" (inclusive)")
            
            if not showall:
                if opt == 0: 
                    showall = True
                    valid = False
                else: 
                    opt -= 1
                    friendlyname = optionsshort_14[opt][0]
                    filename = optionsshort_14[opt][1]
                    retry = False

            else:
                if opt == 0: 
                    showall = False
                    valid = False
                else: 
                    opt -= 1
                    friendlyname = options_14[opt][1]
                    filename = options_14[opt][2]
                    retry = False

        print("Replacing "+friendlyname+" with your generated screensaver...")
        debug(filename)

        renamefile('wd/output_video.mov',"output/"+filename+".mov")
        print("\n\n\nIn 3 seconds, two Finder windows will open: drag the highlighted file "+filename+".mov into the '4KSDR240FPS' folder, clicking Replace if prompted.")

        wait(3)

        callcommand(["open", "/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS"])
        callcommand(["open", "-R", "output/"+filename+".mov"])
    else: renamefile('wd/output_video.mov',"output/"+str(il)+" - "+datetime.datetime.now().strftime("%Y-%m-%d-%H-%m-%s")+".mov")

if loop != 1: print("Videos generated. You'll find them in output/filename.mov.")