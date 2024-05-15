function loadImage(input) {
    var profileImage = document.getElementById('profileImage');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            profileImage.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}