const inputPassword = document.querySelector('#input-password')
const inputRePassword = document.querySelector('#input-re-password')
const eyeImagePass = document.querySelector('.eye-image-pass')
const eyeImageRePass = document.querySelector('.eye-image-re-pass')
const errorPassword = document.querySelector('.errorPassword')



function hideShowSwicher(obj, image){
    if (obj.type === 'password'){
        obj.type = 'text'
        image.src = '/static/images/eye/show.svg'
    }else{
        obj.type = 'password'
        image.src = '/static/images/eye/hide.svg'
    }
}

function checkPasswordMatch(){
    if (inputPassword.value !== inputRePassword.value){
        errorPassword.innerText = 'Passwords do not match';
        return false
    }else{
    errorPassword.innerText = ''
    return true}
}