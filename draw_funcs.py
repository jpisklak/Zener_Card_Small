import pygame


#DRAW INTRO SCREEN TEXT
#=============================================================================
def instr_txt_str():
    txt = "TEST OF EXTRASENSORY PERCEPTION\n\nBACKGROUND\nThis test is designed to evaluate two types of paranormal abilities, precognition and clairvoyance. \nPrecognition is the ability to perceive (and therefore predict) an event that will occur in the future. \nClairvoyance refers to the perception of an object or event without the use of objective sensory input (i.e., without the need of the five senses).\n\nINSTRUCTIONS\nFor this test the computer will shuffle a deck of 5 cards. Each card consists of a unique image (circle, square, star, cross, and wavy-lines). You will be asked to do two things: \n1) Predict which card the computer will select before it has shuffled and drawn from the deck.\n2) Predict which card the computer has selected after it has shuffled and drawn a card.\n\nYou will choose a card by pressing either 1,2,3,4, or 5 on the keyboard according to the legend displayed below. The experiment will last for 100 trials and you can take as much time as you need to make a decision. The experiment can be terminated at any point by pressing the 'Esc' key on your keyboard; however, it is recommended that you complete all 100 trials to create a more robust evaluation of your performance. Your results will be displayed at the end of the test or whenever you hit the 'Esc' (requires minimum of 5 trials).\n\nPress the 'spacebar' key to begin."
    return(txt)



#PRECOG SCREEN TEXT
#=============================================================================
def precog_txt_str():
    txt = "Choose the card that you beleive the computer will select."
    return(txt)


#CLAIRV SCREEN TEXT
#=============================================================================
def clairv_txt_str():
    txt = "The computer has selected a card.\n Choose the card you beleive the computer has selected."
    return(txt)


#FUNCTION FOR WRAPING TEXT
#https://www.pygame.org/pcr/text_rect/index.php #=============================================================================
    
class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        #if accumulated_height + font.size(line)[1] >= rect.height:
            #raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
