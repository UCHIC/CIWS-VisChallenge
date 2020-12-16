# -*- coding: utf-8 -*-
"""
Given a volume of water in gallons, this will generate a graphical representation
of that volume using gallon jugs. The amounts are rounded to the nearest 
quarter gallon
"""
import matplotlib.pyplot as plt
import numpy as np


def icon_plot(amount):
    ''' 
    Plots the amount in gallons using gallon icons. Rounds to nearest 1/4 gallon
    
    Args:
        amount: Amount of water to be visualized in gallons
        
    Returns:
        Figure and Axes array showing the amount of water visualized as gallon jugs
        Further processing is needed on these to get labels, titles, etc.
        For this project, that processing is done by the generate_icon_plots
        function in the data_processing.py file
    '''
    
    # Read in the images used with the plots
    gal = plt.imread('../images/gallon.png')
    three_quart = plt.imread('../images/three_quart.png')
    half_gal = plt.imread('../images/half.png')
    quart = plt.imread('../images/quart.png')
    
    # Set the number of columns for the plots
    columns = 2
    
    # Determine the number of rows needed
    full_rows = int(np.ceil(np.floor(amount)/columns))
    remainder_rows = int(1 - np.ceil(full_rows*columns-amount))
    rows = full_rows + remainder_rows
    
    # Round the amount to quarter gallons
    remainder = np.round((amount - np.floor(amount))*4)/4
    gal_amount = np.floor(amount)
    rounded_amount = gal_amount + remainder
    
    # Due to how matplotlib handles subplots, there needs to be > 1 row
    if rows == 1:
        rows = 2
        empty_top = True
    else:
        empty_top = False
        
    
    fig, ax = plt.subplots(rows,columns,figsize=(columns,rows+1))
    
    # If an extra row was added to appease matplotlib, turn off all the axes
    # Otherwise, axes will be turned off when the image is plotted
    if empty_top == True:
        for col_idx in np.arange(columns-1,-1,-1):
            ax[0,col_idx].axis('off')
        
    # Plot each whole number of gallons
    gal_count = 0;
    if rounded_amount >= 1:
        for row_idx in np.arange(rows-1,-1,-1):
            
            # Turn off axes for row
            for col_idx in np.arange(columns-1,-1,-1):
                ax[row_idx,col_idx].axis('off')
                
            # Plot whole gallons
            for col_idx in np.arange(columns-1,-1,-1):
                ax[row_idx,col_idx].imshow(gal)
                
                gal_count = gal_count + 1
                if gal_count >= gal_amount:
                    break
            if gal_count >= gal_amount:
                break   
            
    
    
    # Determine if the last row is supposed to be empty
    if empty_top:
        row_idx = 1
    else:
        row_idx = 0
    
    # Determine the column position for the remainder
    if gal_count%2 == 0:
        col_idx = 1
        # Turn off other axis on this row
        ax[row_idx,0].axis('off')
    else:
        col_idx = 0

    # Plot the remainder
    if remainder == 0.75:
        ax[row_idx,col_idx].imshow(three_quart)
        ax[row_idx,col_idx].axis('off')
        
    elif remainder == 0.5:
        ax[row_idx,col_idx].imshow(half_gal)
        ax[row_idx,col_idx].axis('off')
        
    elif remainder == 0.25:
        ax[row_idx,col_idx].imshow(quart)
        ax[row_idx,col_idx].axis('off')
        
    else:
        ax[row_idx,col_idx].axis('off')
    
    # Adjust plot so that there is room for a title and x label
    # Labels are not added in this function but space is made that they can be
    # added later
    bottom = .125/(rows+1)
    fig.tight_layout(rect=[0, bottom, 1, 0.95])
    plt.subplots_adjust(wspace=0, hspace=0)
    
    return(fig, ax)
        
if __name__ == "__main__":
    fig, ax = icon_plot(1.3)
