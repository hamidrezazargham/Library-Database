
// verification  
function moveToNextInput(currentInput, nextInputId) {
    if (currentInput.value.length === currentInput.maxLength) {
        document.getElementById(nextInputId).focus();
    }
}
function moveToPreviousInput(currentInput, previousInputId, nextInputId) {
    if (currentInput.value.length === 0) {
        document.getElementById(previousInputId).focus();
    } else if (currentInput.value.length === currentInput.maxLength) {
        document.getElementById(nextInputId).focus();
    }
}
function submitForm() {
    const digit1 = $('#digit1').val();
    const digit2 = $('#digit2').val();
    const digit3 = $('#digit3').val();
    const digit4 = $('#digit4').val();

    const formData = {
        code : digit1+digit2+digit3+digit4
    };

    $.ajax({
        url: '/your-backend-endpoint',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(data) {
            // Handle the response from the backend
            console.log(data);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}