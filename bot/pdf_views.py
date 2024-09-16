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


def generate_pdf2_view(request):
    orders = request.GET.get("orders").split(",")
    orders = Order.objects.filter(pk__in=orders)
    users = ""
    total_sum = 0
    total_qty = 0
    items = []
    inserted_items = []

    for order in orders:
        users += order.user.get_full_name() + ", "
        for item in order.items.all():
            total_sum += float(item.qty) * float(item.price_uzs)
            total_qty += float(item.qty)

            if item.product_id not in inserted_items:
                items.append(
                    {
                        "id": item.product_id,
                        "title": item.product_name,
                        "product_in_set": float(item.product_in_set),
                        "set_amount": float(item.set_amount),
                        "qty": float(item.qty),
                        "price_uzs": float(item.qty) * float(item.price_uzs)
                    },
                    
                )
                inserted_items.append(item.product_id)
            else:
                old_item = next((i for i in items if i["id"] == item.product_id), None)
                new_item = {
                    "id": item.product_id,
                    "title": old_item.get("product_name"),
                    "product_in_set": old_item.get("product_in_set"),
                    "set_amount": old_item.get("set_amount") + float(item.set_amount),
                    "qty": old_item.get('qty') + float(item.qty),
                    "price_uzs": old_item.get("price_uzs") + (float(item.qty) * float(item.price_uzs))
                }
                items.append(new_item)
                items.remove(old_item)
            selected_item = next((i for i in items if i["id"] == item.product_id), None)
            nabor = selected_item['qty'] - int(selected_item["set_amount"] * selected_item["product_in_set"])
            selected_item["case"] = nabor            


    data = {
        "users": users,
        "total_qty": total_qty,
        "total_sum": total_sum,
        "items": items,
    }

    print(data)

    # Render the HTML template with context data
    html_string = render_to_string('contract2.html', {'data': data})

    # Convert HTML to PDF
    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    # Create an HTTP response with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{users}.pdf"'
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
            "agent": f"{obj.agent.get_full_name() if obj.agent else 'net agenta'}",
            "agent_number": str(obj.agent.phone if obj.agent and obj.agent.phone else ""),
            "client": f"{obj.user.get_full_name() if obj.user else 'net klient'}",
            "payment_type": obj.get_payment_type_display(),
            "address": obj.user.territory.first().name if obj.user and obj.user.territory else "net territori",
            "phone": str(obj.user.phone if obj.user and obj.user.phone else ""),
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

