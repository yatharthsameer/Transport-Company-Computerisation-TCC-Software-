from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from mail import sendMail


def bill(consignment):          # generates bill for a consignment in pdf format and mails it to the sender
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
    ptext = '<font size=12>{}</font>'.format("Consignment ID: {}".format(consignment['_id']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Billed To: {}".format(consignment['Sender Name']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Address: {}".format(consignment['Sender Address']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Consignment delivered to: {}".format(consignment['Receiver Name']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Address: {}".format(consignment['Receiver Address']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Phone: {}".format(consignment['Receiver Phone']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Volume of the Consignment: {}".format(consignment['Volume']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size=12>{}</font>'.format("Date of Dispatch: {}".format(consignment['Date Of Dispatch']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>{}</font>'.format("Total Cost Incurred (INR): {}".format(consignment['Cost']))
    Story.append(Paragraph(ptext, styles["Normal"]))
    doc.build(Story)
    sendMail(consignment['Sender Mail'], True)