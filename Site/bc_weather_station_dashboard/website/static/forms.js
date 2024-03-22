//login client side validation
function validateLoginForm() {
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    // Initializing tooltips
    $(username).attr('title', 'Please enter your username').tooltip();
    $(password).attr('title', 'Please enter your password').tooltip();

    if (username.value === '' || password.value === '') {
        $(username).tooltip('show').addClass('validation-error');
        $(password).tooltip('show').addClass('validation-error');
        return false;
    } else {
        $(username).tooltip('hide').removeClass('validation-error');
        $(password).tooltip('hide').removeClass('validation-error');
    }

    return true;
}


//register client side validation
function validateRegisterForm() {
    const username = document.getElementById('registerUsername');
    const email = document.getElementById('registerEmail');
    const password = document.getElementById('registerPassword');
    const confirmPassword = document.getElementById('confirmPassword');
    const phoneNumber = iti.getNumber();

    // E.164 format regex
    const e164Format = /^\+[1-9]\d{1,14}$/;

    // Initializing tooltips
    $(username).tooltip();
    $(email).tooltip();
    $(password).tooltip();
    $(confirmPassword).tooltip();

    if (username.value === '' || email.value === '' || password.value === '') {
        $(username).tooltip('show').addClass('validation-error');
        $(email).tooltip('show').addClass('validation-error');
        $(password).tooltip('show').addClass('validation-error');
        return false;
    } else {
        $(username).tooltip('hide').removeClass('validation-error');
        $(email).tooltip('hide').removeClass('validation-error');
        $(password).tooltip('hide').removeClass('validation-error');
    }

    if (email.value.indexOf('@') === -1) {
        $(email).tooltip('show').addClass('validation-error');
        return false;
    } else {
        $(email).tooltip('hide').removeClass('validation-error');
    }

    if (password.value.length < 8) {
        $(password).tooltip('show').addClass('validation-error');
        return false;
    } else {
        $(password).tooltip('hide').removeClass('validation-error');
    }

    if (password.value !== confirmPassword.value) {
        $(confirmPassword).tooltip('show').addClass('validation-error');
        return false;
    } else {
        $(confirmPassword).tooltip('hide').removeClass('validation-error');
    }

    return true;
}