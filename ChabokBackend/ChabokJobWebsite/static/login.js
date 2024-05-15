$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting in the default way

        // Get form data
        const formData = {
            username: $('#username').val(),
            password: $('#password').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        };
        console.log(formData)

        $.ajax({
            url: 'http://127.0.0.1:8000/login/', // Replace with your actual backend endpoint
            type: 'POST',
            contentType: 'application/json',
            data: formData,
            success: function(data) {
                // Handle the response from the backend
                console.log(data);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});