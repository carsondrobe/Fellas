function validateRegisterForm() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const phoneNumber = iti.getNumber();

    // E.164 format regex
    const e164Format = /^\+[1-9]\d{1,14}$/;

    if (email === '' || password === '' || phoneNumber === '') {
        alert('Please fill in all fields');
        return false;
    }

    if (email.indexOf('@') === -1) {
        alert('Invalid email address');
        return false;
    }

    if (password.length < 8) {
        alert('Password must be at least 8 characters long');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return false;
    }

    if (!iti.isValidNumber() || !e164Format.test(phoneNumber)) {
        alert("Please enter a valid phone number, ensuring it has a country code (e.g. +1)");
        return false;
    }

    return true;
}