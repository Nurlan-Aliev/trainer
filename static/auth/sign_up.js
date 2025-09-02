const errorBox = document.querySelector('.errorBox')
const inputPassword = document.querySelector('#input-password')
const inputRePassword = document.querySelector('#input-re-password')


const AuthForm = document.querySelector('.AuthForm')
AuthForm.addEventListener("submit", Registrate);


function checkPasswordMatch() {
    if (inputPassword.value !== inputRePassword.value) {
        errorBox.innerText = 'Passwords do not match';
        return false
    } else {
        errorBox.innerText = ''
        return true
    }
}

async function Registrate(e) {

    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);



    try {
        const response = await fetch(`/auth/sign_up`, {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            window.location.href = "/";
        } else {
            errorBox.innerText =
                "Брат, такой пользователь уже есть ";
        }

    } catch (err) {
        errorBox.innerText = "Ошибка сети: " + err.message;
    }
}