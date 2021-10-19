import numpy as np
import scipy.stats as sp
#import math as m
import pandas as pd
import matplotlib.pyplot as plt

#A function to...
    #calculate the probability of x hits in y trials trials (Binomial Model)
    #calcualte the expected value of hits
    #calculate the standard deviation of the hits
    #create a plot
#hit = correct choice

#Create function to calculate probability of x hits in y trials trials (Binomial Model)
#hit = correct choice

def binom_prob(subj_data, hit_col, plot_name, plot_title, monitor_res, plot_col):
    attempts = len(subj_data)
    subHits = np.sum(hit_col)
    hit_range = np.arange(0, attempts + 1, 1)
    probHit = 1/5
    
    #The probability of x hits in y trials trials (Binomial Model)
    subject_hitProb = sp.binom.pmf(k = subHits, n = attempts, p = probHit)
    
    #Hit probability across a range of values
    hit_prob = sp.binom.pmf(k = hit_range, n = attempts, p = probHit)
    
    #What is the expected number of hits in x plays?
    exp_hits = attempts * probHit
    subj_data["expectedHits"] = [exp_hits]*len(subj_data) #add to df
    
    #Standard deviation of model
    sd_hits = np.sqrt(attempts * probHit * (1-probHit))
    subj_data["hit_SD"] = [sd_hits]*len(subj_data) #add to df
    
    #plot
    colors = []
    for i in range(len(hit_range)):
        if i == subHits:
            colors.append(plot_col[1])
        else:
            colors.append(plot_col[0])

    img_dpi = 300 #dpi
    img_scale = 2.75#2.25    
    ax_font_size = 4#9
    
    #plt.style.use('seaborn')
    plt.figure(figsize=((monitor_res[0]/img_scale)/img_dpi, 
                        (monitor_res[1]/img_scale)/img_dpi)) 
    plt.bar(hit_range, hit_prob, color = colors, ec = "black", linewidth=.1)

    plt.annotate("*", (subHits, subject_hitProb), ha='center', size = ax_font_size, 
                 color = "red")

    plt.axvline(x = round(exp_hits + sd_hits*1.96, 0) + .5, color = "#808080", linestyle = "--", 
                linewidth = .75)
    plt.axvline(x = round(exp_hits - sd_hits*1.96, 0) - .5, color = "#808080", linestyle = "--", 
                linewidth = .75)
    
    #plt.xticks(np.arange(0, 21, 2), fontsize = ax_font_size)
    xtick = np.arange(0, np.max(hit_range), 5)
    plt.xticks(xtick, fontsize = ax_font_size)
    
    ytick = np.arange(0, np.max(hit_prob), np.round(np.max(hit_prob)/5,3))
    plt.yticks(ytick, fontsize = ax_font_size)
    plt.xlim(round(exp_hits - sd_hits*4, 0), round(exp_hits + sd_hits*4, 0))
    #plt.ylim(0, np.max(hit_prob))
    plt.xlabel("Number of Correct Choices", fontsize = ax_font_size)
    plt.ylabel("Probability", fontsize = ax_font_size)
    plt.title(plot_title, fontsize = ax_font_size)
    plt.savefig(plot_name + '.png', dpi = 300, transparent = False, 
                bbox_inches = 'tight')
    #plt.savefig(plot_name + '.svg')
    #plt.show()
       
    ret_vals = [subHits, subject_hitProb, hit_prob, exp_hits, sd_hits]
    return(ret_vals)


