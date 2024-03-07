function validateLoginForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (email === '' || password === '') {
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

    return true;
}

function validateFeedbackForm() {
    var feedback = document.getElementById('exampleFormControlTextarea1').value;
    if (feedback.trim() === '') {
        alert('Feedback is empty. Please enter your feedback.');
        return false;
    }
    return true;
}