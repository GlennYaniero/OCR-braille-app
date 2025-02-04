import louis
# Louis Braille mapping 
# Glenn Yaniero
table = ["en-us-g1.ctb"]  # Grade 1 Braille table
def text_to_braille(text):
    return louis.translateString(table, text)