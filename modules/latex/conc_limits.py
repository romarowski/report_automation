from modules.latex import unreplace_formula
def info(exceeders):
    text = '\\newcommand{\concLimits}{'
    if not exceeders == []:
        text+='The following pollutants exceeded there considered thresholds '
        for exceeder in exceeders:
            name = unreplace_formula.replace(exceeder.split(' ')[0])
            text += name + ' ; '
    else:
        text+='All pollutants were below their considere thresholds'
    text += '}\n'
    return text
