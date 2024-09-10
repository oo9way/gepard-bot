from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from .models import Order
import zipfile
import os

def generate_pdf_view(request, pk):
    # Get the object from the database
    obj = Order.objects.get(pk=pk)

    data = {
        "id": str(obj.id).zfill(10),
        "order_time": obj.created_at,
        "agent": f"{obj.agent.first_name} {obj.agent.last_name}",
        "agent_number": str(obj.agent.phone if obj.agent.phone else ""),
        "client": f"{obj.user.first_name} {obj.user.last_name}",
        "payment_type": obj.get_payment_type_display(),
        "address": obj.user.territory.first().name,
        "phone": str(obj.user.phone if obj.user.phone else ""),
        "items": obj.items.all(),
    }

    # Render the HTML template with context data
    html_string = render_to_string('contract.html', {'data': data})

    # Convert HTML to PDF
    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    # Create an HTTP response with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="object_{obj.id}.pdf"'
    return response


def generate_multiple_pdfs_view(request):
    ids = request.GET.get('ids').split(',')
    zip_filename = "pdfs.zip"
    temp_dir = "/tmp/generated_pdfs"
    
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Generate PDF for each object
    for pk in ids:
        obj = Order.objects.get(pk=pk)
        data = {
            "id": str(obj.id).zfill(10),
            "order_time": obj.created_at,
            "agent": f"{obj.agent.first_name} {obj.agent.last_name}",
            "agent_number": str(obj.agent.phone if obj.agent.phone else ""),
            "client": f"{obj.user.first_name} {obj.user.last_name}",
            "payment_type": obj.get_payment_type_display(),
            "address": obj.user.territory.first().name,
            "phone": str(obj.user.phone if obj.user.phone else ""),
            "items": obj.items.all(),
        }
        html_string = render_to_string('contract.html', {'data': data})
        pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])
        pdf_filename = os.path.join(temp_dir, f"object_{obj.id}.pdf")
        with open(pdf_filename, 'wb') as pdf_file_out:
            pdf_file_out.write(pdf_file)

    # Add all PDFs to a zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in os.listdir(temp_dir):
            zipf.write(os.path.join(temp_dir, pdf_file), pdf_file)

    # Serve the zip file as an HTTP response
    response = HttpResponse(open(zip_filename, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Cleanup temporary directory
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

    return response

