from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from patients.models import Appointment


@login_required
def doctor_appointments(request):
    if not hasattr(request.user, "doctor_profile"):
        return redirect("pages:home")  # Redirect to a relevant page if user is not a doctor

    appointments = Appointment.objects.all()  # Single doctor sees all appointments
    return render(
        request, "doctor/doctor_appointments.html", {"appointments": appointments}
    )


@login_required
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    if status in dict(Appointment.STATUS_CHOICES):
        appointment.status = status
        appointment.save()
    return redirect("doctor:doctor_appointments")
