import pdfkit as pdfkit
from django.core.files.base import ContentFile
from django.template.loader import get_template

from recepcao.util import Util


def mount_sick_note_pdf(iden, attendance, user, days, days_text, cid, date, until):
    content = get_template('atestadoModel.html').render()


    content = content.replace('rp_name', attendance.patient.name)
    content = content.replace('rp_cns', attendance.patient.cns)
    content = content.replace('doctor_name', user.getCarimbo(user))
    content = content.replace('days', str(days))
    content = content.replace('rp_text', days_text)
    content = content.replace('rp_cid', cid)
    content = content.replace('rp_date', date)
    content = content.replace('until', until)
    content = content.replace('rpc_id', str(iden))
    content = content.replace('rp_today', Util.agora().strftime('%d/%m/%Y'))

    options = {
        'page-size': 'A6',
        'orientation': 'Landscape',
    }

    return pdfkit.from_string(content, False, options=options)
