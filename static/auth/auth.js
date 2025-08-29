const inputPassword = document.querySelector('#input-password')
const inputRePassword = document.querySelector('#input-re-password')
const eyeImagePass = document.querySelector('.eye-image-pass')
const eyeImageRePass = document.querySelector('.eye-image-re-pass')
const errorBox = document.querySelector('.errorBox')

const loginForm = document.querySelector('.loginForm')
loginForm.addEventListener("submit", validatePasswordAndSubmit);


function hideShowSwicher(obj, image) {
    if (obj.type === 'password') {
        obj.type = 'text'
        image.src = '/static/images/eye/show.svg'
    } else {
        obj.type = 'password'
        image.src = '/static/images/eye/hide.svg'
    }
}

function checkPasswordMatch() {
    if (inputPassword.value !== inputRePassword.value) {
        errorBox.innerText = 'Passwords do not match';
        return false
    } else {
        errorBox.innerText = ''
        return true
    }
}


async function validatePasswordAndSubmit(e) {
    e.preventDefault();

    const form = e.target;

    const formData = new FormData(form);

    try {
        const response = await fetch(`/auth/sign_in`, {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            window.location.href = "/";
        } else {
            errorBox.innerText =
                "Брат, ты либо не зареган либо че то не так с твоим логином или паролем ";
        }

    } catch (err) {
        errorBox.innerText = "Ошибка сети: " + err.message;
    }
}