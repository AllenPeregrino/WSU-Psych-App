from fpdf import FPDF
import os
import datetime
import tempfile
from PIL import Image

WIDTH = 210
HEIGHT = 297

class CustomPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.skip_page_number = True

    def header(self):

        #print(f"[HEADER] Skip Page Number: {self.skip_page_number}, Current Page: {self.page_no()}")
        # If it is the first page (title page), skip the page number
        if self.skip_page_number:
            # self.skip_page_number = False
            return

    def footer(self):

            #print(f"[FOOTER] Skip Page Number: {self.skip_page_number}, Current Page: {self.page_no()}")
            if self.skip_page_number or self.page_no() == 1:
                return
            # If this is a title page, skip the footer
            #if not self.skip_page_number:
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            page_number = f'Page {self.page_no() - 1}'
            self.cell(0, 10, page_number, 0, 0, 'C')

# Rotate image and save to a temporary file
def rotate_image_temp(image_path, angle):
    img = Image.open(image_path)
    rotated_img = img.rotate(angle, expand=True)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    rotated_img.save(temp_file.name)
    return temp_file.name

def print_textboxes(pdf, value, descriptions, size):
    pdf.set_font("Arial", "B", 10)
    pdf.ln(11)

    # Merge all text content
    combined_text = ""
    for x in range(size):
        combined_text += "{} {}:\n{}\n\n".format(value, x+1, descriptions[x])

    # Use a single multi_cell call to generate a large box containing all the content
    pdf.set_fill_color(211, 221, 235) # color in the box
    pdf.multi_cell(w=75, h=5, txt=combined_text, border=1, align="L", fill=1)

    pdf.set_font("Arial", "", 10) # reset font to not bold

def print_feedback_box(pdf, feedback, x=10, y=None, w=75, font_size=10):
    # 在PDF中打印无边框的反馈文本框
    if y is not None:
        pdf.set_y(y)  # 设置y坐标

    start_x = pdf.get_x()  # 获取起始x坐标
    start_y = pdf.get_y()  # 获取起始y坐标

    # 设置统一的字体和大小
    pdf.set_font("Arial", "", font_size)

    feedback_lines = feedback.split('\n')
    for line in feedback_lines:
        pdf.multi_cell(w=w, h=4, txt=line, border=0, align="L")  # 设置border=0去除边框

def print_feedback_box_horizontal(pdf, feedback, x=10, y=None, w=180, font_size=10,offset_y=20):
    # Print horizontally aligned feedback text boxes in PDF
    if y is not None:
        pdf.set_y(y)  # Set the y coordinate

    pdf.set_x(x)  # Set the x coordinate
    pdf.set_font("Arial", "", font_size)  # Set font once, with the specified size

    feedback_lines = feedback.split('\n')

    # line below is to avoid the x axis labels covering up the text
    pdf.ln(5)  # Adjust this value as needed

    # Print feedback text using multi_cell for automatic line wrapping, no border
    for line in feedback_lines:
        pdf.multi_cell(w=w, h=5, txt=line, border=0, align="L")

def add_name(pdf, name):
    pdf.set_font('Arial', 'B', 30)
    pdf.ln(50)
    pdf.cell(0, 10, "Person in Context Assessment:", 0, 0, 'C')
    pdf.ln(15)
    pdf.cell(0, 10, "A Personality Assessment of", 0, 0, 'C')
    pdf.ln(15)
    pdf.cell(0, 10, "Temperament, Self-Concept,", 0, 0, 'C')
    pdf.ln(15)
    pdf.cell(0, 10, "Personal Goals and Standards", 0, 0, 'C')
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(30)
    pdf.cell(0, 10, name, 0, 0, 'C')
    pdf.ln(15)
    today = datetime.date.today()
    d = today.strftime("%B %d, %Y")
    dr = "Date of Report: %s" % (d)
    pdf.cell(0, 10, dr, 0, 0, 'C')

def section_headers(pdf, text):
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 0, text, 0, 0, 'C')
    #pdf.text(x=WIDTH/2, y=14, txt=text)

def temperament_scaling(pdf, y_position=0):
    pdf.set_font('Arial', "", 10)
    base_y = y_position - 45  # Adjust as needed to position labels correctly
    pdf.text(x=5, y=base_y, txt="Very High")
    pdf.text(x=5, y=base_y + 33, txt="Average")  # 2.5
    pdf.text(x=5, y=base_y + 66, txt="Very Low")

# Comparison figure
def comparison_figure(pdf, path, ranks, goals):
    pdf.add_page()

    comparison_image_path = os.path.join(path, 'Comparison.png')
    arrow_image_path = os.path.join(path, 'Arrow.png')
    single_arrow_image_path = os.path.join(path, 'Single_Arrow.png')

    # Change font and add titles
    pdf.set_font('Arial', '', 16)
    pdf.text(x=48, y=14, txt="Most Important Goals and Ranking of Values:")
    pdf.text(x=57, y=20, txt="Do Your Goals Reflect Your Values?")

    # Add PERSONAL VALUES title in bold
    pdf.set_font("Arial", "B", 11)
    pdf.set_xy(10, 25) # changed to 25 from 35
    pdf.cell(0, 5, "Personal Values", ln=True, align="C")

    ps_text = ("     The last personality component we assessed was your values. Your values refer to your beliefs about what you believe is important to living a good life. To measure your values, you ranked them in order of their importance to you in living a good life.")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0,5, ps_text, border=0, align="L")
    pdf.ln(1)

    ps_text2 = ("     Research suggests that is important to have personal goals that match your values. Think about whether the goals you are striving for reflect what you believe is most important to living well. If you have a number of values that you listed as important for which you do not list any goals, this may indicate poor goal-value fit. If it is the case that you do not have goals for your most important values, you might consider developing a new goal for those values. Research has shown that having goals that match our values increases psychological well-being and motivation.")
    pdf.multi_cell(0, 5, ps_text2, border=0, align="L")
    pdf.ln(1)

    if os.path.exists(comparison_image_path):
        pdf.image(comparison_image_path, x=-23, y=35, w=WIDTH + 50, h=180 + 30)
    else:
        print(f"Comparison image not found at {comparison_image_path}")

    rotated_arrow_path = rotate_image_temp(arrow_image_path, angle=90)
    if rotated_arrow_path:
        pdf.image(rotated_arrow_path, x=(WIDTH / 2) - 31, y=(HEIGHT / 2) - 37, w=35, h=40)
        os.remove(rotated_arrow_path)  # Clean up the temporary file
    else:
        print(f"Arrow image not found at {arrow_image_path}")

    if os.path.exists(single_arrow_image_path):
        pdf.image(single_arrow_image_path, x=-19, y=(HEIGHT / 2) + 32 - 130, w=75, h=145)
    else:
        print(f"Single arrow image not found at {single_arrow_image_path}")

    pdf.set_font("Arial", "B", 14)
    pdf.text(x=112, y=83, txt="Your 4 Most Important Goals:")
    pdf.text(x=37, y=83, txt="Your Ranking of Values:")
    pdf.set_font('Arial', '', 14)
    pdf.text(x=16, y=(HEIGHT/2)+43+13-120, txt="Most")
    pdf.text(x=11, y=(HEIGHT/2)+47+13-120, txt="Important")
    pdf.text(x=16, y=(HEIGHT/2)+121+13-95, txt="Least")
    pdf.text(x=11, y=(HEIGHT/2)+125+13-95, txt="Important")

    # Format Rankings
    output = ""
    for item in ranks:
        output += f"{item}\n"

    # Adding text to the boxes
    pdf.set_font('Arial', '', 11)

    # Add ranking of values to the PDF
    pdf.set_xy(x=42, y=97)
    pdf.multi_cell(w=100, h=8, txt="{}".format(output[0:-1]), border=0)

    pdf.set_xy(x=111, y=97.8)
    # Join the goals list with new lines
    goals_text = "\n\n\n".join([f"Goal {i + 1}: {goal}" for i, goal in enumerate(goals)])

    # Add goals to the PDF
    pdf.multi_cell(w=85, h=5, txt=goals_text, border=0)

def add_sort(pdf, order):
    pdf.add_page()
    #count = 0

    pdf.set_font('Arial', 'B', 20)
    pdf.text(x=7, y=15, txt="Personalized Client Centered Treatment Recommendations")
    facet = [order[0]]
    yIdx = 30
    pdf.set_font('Arial', '', 15)
    pdf.text(x=23, y=yIdx, txt="Additional information on these reccomended treatments can be")
    pdf.text(x=23, y=yIdx+5, txt="found at https://div12.org/treatments/.")

    yIdx = 50

    for i, f in enumerate(facet):
        z = f.split("\n")
        #reccomendations
        pdf.set_font('Arial', 'B', 18)
        pdf.text(x=20, y=yIdx, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', 'B', 15)
        pdf.text(x=25, y=yIdx+5, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', '', 13)
        pdf.text(x=25, y=yIdx+10, txt=z[0])
        z.pop(0)
        pdf.text(x=25, y=yIdx+15, txt=z[0])
        z.pop(0)

        #factors of interest
        if len(z) > 1:
            pdf.set_font('Arial', 'B', 15)
            pdf.text(x=25, y=yIdx+25, txt=z[0])
            z.pop(0)
            yIdx = yIdx+30
            pdf.set_font('Arial', '', 13)
            for z1 in z:
                pdf.text(x=25, y=yIdx, txt=z1)
                yIdx += 5

        if i == 0: #+60
            yIdx = 90
        elif i == 1:
            yIdx = 150

    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.text(x=23, y=15, txt="Treatment Recommendations: Situation Specific")
    facet = [order[2], order[3], order[4], order[5]]
    yIdx = 30

    for i, f in enumerate(facet):
        z = f.split("\n")
        #reccomendations
        pdf.set_font('Arial', 'B', 18)
        pdf.text(x=20, y=yIdx+5, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', 'B', 15)
        pdf.text(x=25, y=yIdx+10, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', '', 13)
        pdf.text(x=25, y=yIdx+15, txt=z[0])
        z.pop(0)
        pdf.text(x=25, y=yIdx+20, txt=z[0])
        z.pop(0)

        #factors of interest
        if len(z) > 1:
            pdf.set_font('Arial', 'B', 15)
            pdf.text(x=25, y=yIdx+30, txt=z[0])
            z.pop(0)
            yIdx = yIdx+35
            pdf.set_font('Arial', '', 13)
            for z1 in z:
                pdf.text(x=25, y=yIdx, txt=z1)
                yIdx += 5

        if i == 0: #+55
            yIdx = 85
        elif i == 1:
            yIdx = 140
        elif i == 2:
            yIdx = 195


    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.text(x=23, y=15, txt="Treatment Recommendations: Situation Specific")
    facet = [order[7], order[8], order[9], order[10]]
    yIdx = 30

    for i, f in enumerate(facet):
        z = f.split("\n")
        #reccomendations
        pdf.set_font('Arial', 'B', 18)
        pdf.text(x=20, y=yIdx+5, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', 'B', 15)
        pdf.text(x=25, y=yIdx+10, txt=z[0])
        z.pop(0)
        pdf.set_font('Arial', '', 13)
        pdf.text(x=25, y=yIdx+15, txt=z[0])
        z.pop(0)
        pdf.text(x=25, y=yIdx+20, txt=z[0])
        z.pop(0)

        #factors of interest
        if len(z) > 1:
            pdf.set_font('Arial', 'B', 15)
            pdf.text(x=25, y=yIdx+30, txt=z[0])
            z.pop(0)
            yIdx = yIdx+35
            pdf.set_font('Arial', '', 13)
            for z1 in z:
                pdf.text(x=25, y=yIdx, txt=z1)
                yIdx += 5

        if i == 0: #+55
            yIdx = 85
        elif i == 1:
            yIdx = 140
        elif i == 2:
            yIdx = 195
