$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting in the default way

        // Get form data
        const formData = {
            username: $('#username').val(),
            password: $('#password').val()
        };

        $.ajax({
            url: 'http://127.0.0.1:8000/login/', // Replace with your actual backend endpoint
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(data) {
                // Handle the response from the backend
                console.log(data);
                window.location.href = 'main.html';
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});