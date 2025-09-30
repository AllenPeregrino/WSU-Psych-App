from fpdf import FPDF
WIDTH = 210
HEIGHT = 297


def print_textboxes(pdf, value, descriptions, size):
    pdf.set_font("Arial", "", 10)
    pdf.ln(0)
    lineholder = 0
    d = "I wandered lonely as a phone\nThat floats on high o'er vales and hills,\nWhen all at once I saw a crowd,\nA host, of golden daffodils\nBeside the lake, beneath the trees,\nFluttering and dancing in the breeze."
    for x in range(size):
        pdf.multi_cell(w=75,h=5,txt="{} {}:\n{}".format(value, x+1, descriptions[x]), border = 1, align="L")
        lineholder += 72
        pdf.set_y(lineholder)

def create_title(pdf, title):
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(150)
    pdf.cell(0, 10, title, 0, 0, 'C')
    pdf.ln(20)

def write_body(pdf, body):
    pdf.set_font('Arial', "", 12)
    lineholder = 150
    pdf.set_y(150)
    for k,v in body.items():
        pdf.set_x(25)
        pdf.multi_cell(w=WIDTH-60,h=5,txt="{}: {}\n".format(k, v), border = 0, align="L")
        lineholder += 10
        pdf.set_y(lineholder)

def create_header(pdf, header):
    pdf.set_font('Arial', '', 16)
    pdf.write(5, f'{header}')

# Comparison figure
def comparison_figure(pdf, path, ranks, goals):
    pdf.add_page()
    pdf.image(path + "/images/Comparison.png", x=0, y=0, w=WIDTH+5, h=170) #(HEIGHT/2)+30
    pdf.image(path + "/images/Comparison.png", x=0, y=(HEIGHT/2), w=WIDTH+5, h=170) #(HEIGHT/2)+30
    pdf.image(path + "/images/Arrow.png", x=(WIDTH/2)-47, y=(HEIGHT/2)-42, w=100, h=100)
    pdf.image(path + "/images/Single_Arrow.png", x=0, y=(HEIGHT/2)+18, w=75, h=110)

    # Change font and add titles
    pdf.set_font('Arial', '', 16)
    pdf.text(x=48, y=14, txt="Most Important Goals and Ranking of Values:")
    pdf.text(x=57, y=20, txt="Do Your Goals Reflect Your Values?")
    pdf.text(x=70, y=43, txt="Your 4 Most Important Goals:")
    pdf.text(x=76, y=(HEIGHT/2)+43, txt="Your Ranking of Values:")
    pdf.set_font('Arial', '', 14)
    pdf.text(x=36, y=(HEIGHT/2)+43, txt="Most")
    pdf.text(x=31, y=(HEIGHT/2)+47, txt="Important")
    pdf.text(x=36, y=(HEIGHT/2)+121, txt="Least")
    pdf.text(x=31, y=(HEIGHT/2)+125, txt="Important")


    # Format Rankings
    output = ""
    for item in ranks:
        output += f"{item}\n"

    # Adding text to the boxes
    pdf.set_font('Arial', '', 10)
    pdf.set_xy(x=30, y=50)
    pdf.multi_cell(w=150, h=18, txt="Goal 1: {}\nGoal 2: {}\nGoal 3: {}\nGoal 4: {}".format(goals[0], goals[1], goals[2], goals[3]), border=0)
    pdf.set_font('Arial', '', 11)
    pdf.set_xy(x=70, y=200)
    pdf.multi_cell(w=100, h=8, txt="{}".format(output[0:-1]), border=0)