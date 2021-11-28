from fpdf import FPDF
import datetime

def create_pdf(donor, date, donation_euros, exchange_rate, donation_tomans, receipt_image):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', size = 12)
    __add_line(pdf, donor)
    __add_line(pdf, date)
    __add_line(pdf, f'Donation in Euros: {donation_euros}')
    __add_line(pdf, f'Euro to Toman exchange currency rate: {exchange_rate}')
    __add_line(pdf, f'Donation in Tomans: {donation_tomans}')
    pdf.image(receipt_image, w=100, h=100)
    pdf_path = get_tmp_file_dir('pdf')
    pdf.output(pdf_path)
    print('PDF created sucessfully')
    return pdf_path


def __add_line(pdf, line):
    pdf.cell(200, 10, txt = line, ln = 2, align = 'L')


def get_tmp_file_dir(extension='None'):
    current_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    file_extension = f'.{extension}' if extension != 'None' else ''
    tmp_file_dir = f'/tmp/{current_date_time}{file_extension}'
    return tmp_file_dir

