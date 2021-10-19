import pygame
import random
import time
import pandas as pd
import numpy as np

import draw_funcs
import data_funcs


#INITIALIZE PYGAME
pygame.init()
SubjectID = round(time.time())
black = [0,0,0]
white = [255, 255, 255]


#SET MONITOR
win = pygame.display.set_mode([800, 600])
#monitor_res = pygame.display.get_surface().get_size()
monitor_res = [800, 600]
pygame.display.set_caption("Zener Card Experiment")


#SHUFFLE CARDS SO SUBJECTS GET DIFFERENT/RANDOMIZED INPUT ORDERS FOR EACH ATTEMPT
cards = ["circle", "square", "cross", "star", "lines"]
random.shuffle(cards)


#LOAD CARD LEGEND
card_size = [352, 538]
card_size_new = [int(card_size[0]/4), int(card_size[1]/4)]

# A dictionary to store the images with names
card_images = {}
# Loop through image names, construct the filename and load them as Surfaces
for name in cards:
    filename = "./Stims/" + name + '.tif'
    card_images[name] = pygame.image.load(filename)
    card_images[name] = pygame.transform.smoothscale(card_images[name], card_size_new)

card_adj = monitor_res[0]*(1/5)
card_half_width = card_size_new[0] / 2
card_pos = [
            int(monitor_res[0]/2 - card_adj*2 - card_half_width),
            int(monitor_res[0]/2 - card_adj - card_half_width),
            int(monitor_res[0]/2 - card_half_width),
            int(monitor_res[0]/2 + card_adj - card_half_width),
            int(monitor_res[0]/2 + card_adj*2 - card_half_width) 
            ]


#LOAD THE BACK OF THE CARD FOR DISPLAY
card_back = pygame.image.load("./Stims/cardBack.tif")
#card_back_size = [int(card_size[0]/6), int(card_size[1]/6)]
card_back_size = [card_size_new[0], card_size_new[1]]
card_back = pygame.transform.smoothscale(card_back, card_back_size)
card_back_pos = [(monitor_res[0]/2) - (card_back_size[0]/2),
                 (monitor_res[1]/2.5) - (card_back_size[1]/2)]


#BASIC PARAMETERS
trial_amount = 100
trial_count = 1


#LISTS FOR DATA STORE
preCogRespKey = []
preCogRespCard = []
preCogRT = []

cardSelected = []
clairvRespKey = []
clairvRespCard = []
clairvRT = []

subj_col = []
trial_col = []   
df = pd.DataFrame()


#LOAD TEXT FOR DISPLAY
#Card Legend Number
font = pygame.font.SysFont("Consolas", 20)
card_num = {}
keys = ["1", "2", "3", "4", "5"]
for key in keys:
    card_num[key] = font.render(key, True, black, white)
    
#Intro Text Load
intro_txt_font = pygame.font.SysFont("Consolas", 13)
intro_txt_rect = pygame.Rect(20, 
                              20, 
                              monitor_res[0]-20*2, 
                              monitor_res[1]-20*(1/2)) #left, top, width, height

intro_txt_rend = draw_funcs.render_textrect(draw_funcs.instr_txt_str(), 
                                            intro_txt_font, 
                                            intro_txt_rect, 
                                            black, white, 
                                            1)

#Precog Text Load
precog_txt_rect = pygame.Rect(50, 
                              150, 
                              monitor_res[0]-50*2, 
                              monitor_res[1]-50*2)

precog_txt_rend = draw_funcs.render_textrect(draw_funcs.precog_txt_str(),
                                            font,
                                            precog_txt_rect,
                                            black, white,
                                            1)

#Clairv Text Load
clairv_txt_rect = pygame.Rect(50, 
                              100, 
                              monitor_res[0]-50*2, 
                              monitor_res[1]-50*2)

clairv_txt_rend = draw_funcs.render_textrect(draw_funcs.clairv_txt_str(),
                                            font,
                                            clairv_txt_rect,
                                            black, white,
                                            1)

#Trial Counter Text Load
#trial_txt_rect = pygame.Rect(10,5, 400, 200)
trial_txt_rect = pygame.Rect(10,5, 200, 50)


#INTRO SCREEN LOOP
#-----------------------------------
intro_run = True

while intro_run:
    win.fill([255, 255, 255])
    
    #Allows for the "x" corner button to be pressed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    #Intro Text Display
    win.blit(intro_txt_rend, intro_txt_rect.topleft)        
    
    #Card Legend Display
    #win.blit(card_images['circle'], (100, 100))
    count = 0
    for i in card_images:
        win.blit(card_images[i], (card_pos[count], monitor_res[1]*(4/6)))
                                  #550))
        win.blit(card_num[str(count + 1)], 
                          [card_pos[count] + card_half_width,
                           monitor_res[1]/1.1])
                           #monitor_res[1]* (7/8)])
                           #monitor_res[1]-50*(1/2)])
        count = count + 1
        
    pygame.display.update()


    #Get Spacebar press
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        intro_run = False



#TESTING PHASE LOOP
#-----------------------------------
main_task_run = True
phase = 1 #1 = PreCog, -1 = clairv
response_made = False
clock = pygame.time.Clock()
RT = 0
keyNum = 0

while main_task_run:
    win.fill([255, 255, 255])
    clock.tick(60)
    
    #Allows for the "x" corner button to be pressed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_task_run = False
    
    
    #PreCog Text Displays
    if phase == (1):
        #Text Display
        win.blit(precog_txt_rend, precog_txt_rect.topleft)
        
        #Trial Display
        trial_txt = "Trial: " + str(round(trial_count))

        trial_txt_rend = draw_funcs.render_textrect(trial_txt,
                                            font,
                                            trial_txt_rect,
                                            black, white,
                                            0)
        
        win.blit(trial_txt_rend, trial_txt_rect.topleft) 
        
     #Clair Text Displays
    elif phase == (-1):
        #Text Display
        win.blit(clairv_txt_rend, clairv_txt_rect.topleft)
        
        #Trial Display
        win.blit(trial_txt_rend, trial_txt_rect.topleft)
        
        #Card Back Display
        win.blit(card_back, card_back_pos) 

    #Card Legend Display
    count = 0
    for i in card_images:
        win.blit(card_images[i], (card_pos[count], monitor_res[1]*(4/6)))
        win.blit(card_num[str(count + 1)],
                 [card_pos[count] + card_half_width,
                  monitor_res[1]/1.1])
                  #monitor_res[1]* (7/8)])
        count = count + 1

    #Display Update
    pygame.display.update()
    press_time_start = pygame.time.get_ticks()

    #Get Key press
    while response_made == False:
        events = pygame.event.get()
        #print(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    press_time_stop = pygame.time.get_ticks()
                    RT = (press_time_stop - press_time_start)
                    keyNum = 1
                    response_made = True
                    
                elif event.key == pygame.K_2:
                    press_time_stop = pygame.time.get_ticks()
                    RT = (press_time_stop - press_time_start)
                    keyNum = 2
                    response_made = True
                    
                elif event.key == pygame.K_3:
                    press_time_stop = pygame.time.get_ticks()
                    RT = (press_time_stop - press_time_start)
                    keyNum = 3
                    response_made = True
                    
                elif event.key == pygame.K_4:
                    press_time_stop = pygame.time.get_ticks()
                    RT = (press_time_stop - press_time_start)
                    keyNum = 4
                    response_made = True
                    
                elif event.key == pygame.K_5:
                    press_time_stop = pygame.time.get_ticks()
                    RT = (press_time_stop - press_time_start)
                    keyNum = 5
                    response_made = True
                    
                elif event.key == pygame.K_ESCAPE and trial_count > 5:
                    main_task_run = False
                    response_made = True

                elif event.key == pygame.K_ESCAPE and trial_count <= 5:
                    pygame.quit()

            elif event.type == pygame.QUIT:
                pygame.quit()



    
    if response_made == True and main_task_run == True:
        
        #Save Data
        if phase == 1:
            preCogRespKey.append(keyNum)
            preCogRespCard.append(cards[(keyNum - 1)])
            preCogRT.append(RT)
            subj_col.append(SubjectID)
            trial_col.append(trial_count)  
            
            #Shuffle and Pick a Card
            card_select = random.choice(cards)
            cardSelected.append(card_select)
            
        elif phase == (-1):
            clairvRespKey.append(keyNum)
            clairvRespCard.append(cards[(keyNum - 1)])
            clairvRT.append(RT)
            
            #Store Data
            data_dict = {
                'Subject': subj_col,
                #'Age': age,
                #'Sex': sex,
                'Trial': trial_col,
                'preCogRespKey': preCogRespKey, 
                'preCogRespCard': preCogRespCard, 
                'preCogRT': preCogRT,
                'cardSelected': cardSelected,
                'clairvRespKey': clairvRespKey,
                'clairvRespCard': clairvRespCard,
                'clairvRT': clairvRT
                #'q1': q1_ans,
                #'q2': q2_ans,
                #'email': q3_ans
                }
            subj_data = pd.DataFrame(data_dict)
            
            subj_data.to_csv("./Data/ZenerStudy" + str(SubjectID) + ".csv",
                             index = False,
                             header=True
                             )

        #Trial and Phase Adjust
        phase = phase * (-1)
        trial_count = (trial_count + 0.5)
        response_made = False
        if trial_count == (trial_amount + 1):
            main_task_run = False
            


#ANALYSIS CALCULATIONS
#-----------------------------------
#Obtain Correct Responses
preCogCorrect = subj_data["preCogRespCard"] == subj_data["cardSelected"]
clairvCorrect = subj_data["clairvRespCard"] == subj_data["cardSelected"]
subj_data["preCogCorrect"] = preCogCorrect.astype(int)
subj_data["clairvCorrect"] = clairvCorrect.astype(int)
propCorrPreCog = np.mean(preCogCorrect)
propCorrClairv = np.mean(clairvCorrect)  

preCog_results = data_funcs.binom_prob(subj_data = subj_data, 
                                       #hit_col = "preCogCorrect", 
                                       hit_col = preCogCorrect, 
                                       plot_name = "preCogPlot", 
                                       plot_title = "Precognition Score",
                                       #plot_col = ["#4c72b0", "#dd8452"],
                                       #plot_col = ["#808080", "#dd8452"],
                                       plot_col = ["#808080", "red"],
                                       monitor_res = monitor_res)

clairv_results = data_funcs.binom_prob(subj_data = subj_data, 
                                       #hit_col = "clairvCorrect", 
                                       hit_col = clairvCorrect, 
                                       plot_name = "clairvPlot", 
                                       plot_title = "Clairvoyance Score",
                                       #plot_col = ["#55a868", "#c44e52"],
                                       #plot_col = ["#808080", "#c44e52"],
                                       plot_col = ["#808080", "red"],
                                       monitor_res = monitor_res)
    
#Saving Calculated Values
subj_data.to_csv("./Data/ZenerStudy" + str(SubjectID) + ".csv", 
                 index = False,
                 header = True
                 )

#Load Graphs
preCogResultImg = pygame.image.load("preCogPlot.png")
clairvResultImg = pygame.image.load("clairvPlot.png")
#plot_size = [862,593]
plot_size = [368, 322]

#Load Text
result_txt_font = pygame.font.SysFont("Consolas", 16)
result_txt_rect = pygame.Rect(20, 
                              20, 
                              monitor_res[0]-20*2, 
                              monitor_res[1]-20*2) #left, top, width, height


result_txt_1 = "The experiment is complete. Press the ESC key to exit.\n\nPrecognition Results:"
    
result_txt_2 = "\nYou chose correctly " + str(preCog_results[0]) + " times (" + str(round((propCorrPreCog * 100), 2)) + "%.)" 

result_txt_3 = "\n\nClairvoyance Results: \nYou chose correctly " + str(clairv_results[0]) + " times (" + str(round((propCorrClairv * 100), 2)) + "%.)"

result_txt_4 = "\n\nBy guessing randomly you would expect to be, on average, correct " + str(round(subj_data["expectedHits"][0], 0)) + " out of every " + str(len(subj_data)) + " attempts (" + str(round(round(subj_data["expectedHits"][0],0)/len(subj_data) * 100, 2)) + "%). The red bar on the graphs show the probability of obtaining your exact results. Values falling outside the dashed lines are typically considered rare. A person who possess either precognitive abilities or clairvoyance would be expected to produce at least " + str(round(preCog_results[3] + (preCog_results[4] * 2) + 1, 0)) + " correct choices. Further, upon re-taking this test they should (all things being equal) be able to reproduce that result."

result_txt = result_txt_1 + result_txt_2 + result_txt_3 + result_txt_4

result_txt_rend = draw_funcs.render_textrect(result_txt, 
                                            result_txt_font, 
                                            result_txt_rect, 
                                            black, white, 
                                            1)
 


#ANALYSIS PHASE LOOP
#-----------------------------------   
analysis_run = True

while analysis_run == True:
    win.fill([255, 255, 255])
    
    #Allows for the "x" corner button to be pressed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            analysis_run = False
            
    #Display Text
    win.blit(result_txt_rend, result_txt_rect.topleft)  
    
    #Display Graphs
    #win.blit(preCogResultImg, (20, monitor_res[1]-75 - plot_size[1] ))
    #win.blit(clairvResultImg, (monitor_res[0] - 50 - plot_size[0],
                               #monitor_res[1]-75 - plot_size[1] ))
    win.blit(preCogResultImg, (0, monitor_res[1]/2.25 ))
    win.blit(clairvResultImg, (monitor_res[0] - plot_size[0] - 40,
                               monitor_res[1]/2.25))
      

    pygame.display.update()         




    #Get Spacebar press
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        analysis_run = False
            

pygame.quit()
