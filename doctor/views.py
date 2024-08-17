from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorAppointment
from patients.models import Appointment
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.conf import settings
import os
from django.views.decorators.http import require_POST
from contact.forms import ContactForm
from contact.models import Contact
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def doctor_appointments(request):
    if request.user.role == "doctor" or "Doctor":
        appointments = DoctorAppointment.objects.filter(doctor=request.user).order_by(
            "-date"
        )
        patient_appointments = Appointment.objects.filter(doctor=request.user)

        # Add flags to indicate whether the status allows for editing
        for appointment in patient_appointments:
            appointment.can_edit = appointment.status not in ["completed", "canceled"]

        return render(
            request,
            "doctor/doctor_appointments.html",
            {
                "appointments": appointments,
                "patient_appointments": patient_appointments,
            },
        )
    else:
        return redirect("pages:authenticated_home")


@login_required
@require_POST
def update_appointment_status(request, pk):
    if request.user.role != "doctor" or "Doctor":
        return redirect("pages:authenticated_home")

    appointment = get_object_or_404(DoctorAppointment, pk=pk, doctor=request.user)
    status = request.POST.get("status")

    if status in ["completed", "canceled"]:
        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment status updated to {status}.")
    else:
        messages.error(request, "Invalid status.")

    return redirect("doctor:doctor_appointments")


def static_file_debug(request):
    try:
        with open(
            os.path.join(settings.BASE_DIR, "static", "icon", "favicon.ico"), "rb"
        ) as f:
            return HttpResponse(f.read(), content_type="image/x-icon")
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


def doctor_contact(request):
    # Check if the user is a doctor; use .lower() to handle case-insensitivity
    if request.user.role.lower() != "doctor":
        return redirect("pages:authenticated_home")  # Redirect to a general home page if not a doctor

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.recipient_role = "doctor"  # Set the recipient role to 'doctor'

            # Determine recipient based on recipient_role
            recipient_role = form.cleaned_data.get("recipient_role")
            if recipient_role == "doctor":
                # Find a recipient doctor user; you might want to select a specific doctor or all doctors
                # For simplicity, selecting the first doctor user. Adjust based on your needs.
                contact.recipient = User.objects.filter(role='doctor').first()
            elif recipient_role == "patient":
                # In case recipient_role is "patient", you might want to set the recipient to a specific patient.
                # For instance, you can set it to a patient user or based on another logic.
                contact.recipient = User.objects.filter(role='patient').first()  # Adjust as necessary

            if contact.recipient is None:
                # Handle the case where no recipient is found
                form.add_error(None, "No recipient found based on the recipient role.")
                return render(request, "doctor/doctor_contact.html", {"form": form})

            contact.save()
            return redirect("doctor:doctor_messages")  # Redirect to the doctor messages page or a success page
    else:
        form = ContactForm(request=request)

    return render(request, "doctor/doctor_contact.html", {"form": form})

@login_required
def doctor_messages(request):
    # Check if the user's role is exactly "doctor" or "Doctor"
    if request.user.role.lower() not in ["doctor"]:
        return redirect("pages:authenticated_home")

    messages = Contact.objects.filter(recipient_role="patient", user=request.user)
    return render(request, "doctor/messages.html", {"messages": messages})
