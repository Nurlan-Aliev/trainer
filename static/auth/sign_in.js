const errorBox = document.querySelector('.errorBox')
const inputPassword = document.querySelector('#input-password')


const loginForm = document.querySelector('.loginForm')
loginForm.addEventListener("submit", validatePasswordAndSubmit);

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