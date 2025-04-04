document.getElementById('refresh-captcha').addEventListener('click', function(){
    var captchaImage = document.getElementById('captcha-image');
    captchaImage.src = '/captcha_image?' + Date.now();
});