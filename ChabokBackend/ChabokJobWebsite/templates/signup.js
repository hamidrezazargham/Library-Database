$(document).ready(function() {
    $('#signupForm').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting in the default way

        // Get form data
        const formData = {
            username: $('#username').val(),
            email: $('#email').val(),
            password1: $('#password1').val(),
            password2: $('#password2').val(),
            role: $('input[name=inlineRadioOptions]:checked').val()
        };

        // Post form data to the backend
        $.ajax({
            url: 'http://127.0.0.1:8000/signup/', // Replace with your actual backend endpoint
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            
            success: function(data) {
                // Handle the response from the backend

                console.log(data);
                window.location.href = 'login.html';
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});