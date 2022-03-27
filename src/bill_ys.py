<<<<<<< HEAD
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


def bill(consignment):
    Story = []
    doc = SimpleDocTemplate( "bill.pdf" , pagesize = A4 )
    styles = getSampleStyleSheet()
    title_style = styles[ "Heading1" ]
    title_style.alignment = 1
    title = Paragraph( "TCC Billing" , title_style )
    Story.append( title )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=1))
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Consignment ID: ", " ", consignment['_id'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Billed To: {}".format(consignment['Sender Name']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Address: {}".format(consignment['Sender Address']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Consignment delivered to: ", " ", consignment['Receiver Name'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Address: ", " ", consignment['Receiver Address'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Phone: ", " ", consignment['Receiver Phone'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Volume of the Consignment: ", " ", consignment['Volume'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Date of Dispatch: ", " ", consignment['Date Of Dispatch'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Total Cost Incurred (INR): ", " ", consignment['Cost'])
    Story.append(Paragraph(ptext, styles["Normal"]))
    doc.build(Story)
=======
# Python program to create
# a pdf file


from fpdf import FPDF


# save FPDF() class into a
# variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size=15)

# create a cell
pdf.cell(200, 10, txt="hello everyone",
         ln=1, align='C')

# add another cell
pdf.cell(200, 10, txt="This is a pdf file",
         ln=2, align='C')

# save the pdf with name .pdf
pdf.output("Hello.pdf")
>>>>>>> d6a76a4654aaa7d65de0ae9ea8a534bc9ab23b13
