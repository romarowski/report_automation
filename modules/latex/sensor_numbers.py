import numpy as np
import inflect
def number(sites):
    count = np.size(sites)
    p = inflect.engine()
    nbr = p.number_to_words(count)
    text = '\\newcommand{\stationsnbr}{'+nbr.capitalize()+'}\n'
    return text
    
