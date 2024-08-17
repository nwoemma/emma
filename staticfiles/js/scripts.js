$(document).ready(function() {
    $('#appointment-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: "{% url 'patients:patient_appointments' %}",
            type: "POST",
            data: $(this).serialize(),
            success: function(response) {
                // Handle success - update the appointments table
                $('#appointments-table-body').html($(response).find('#appointments-table-body').html());
                $('#appointment-form')[0].reset(); // Clear the form
            },
            error: function(response) {
                // Handle error
                console.error('An error occurred:', response);
            }
        });
    });
});