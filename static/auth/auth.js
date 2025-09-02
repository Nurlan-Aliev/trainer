const eyeImagePass = document.querySelector('.eye-image-pass')
const eyeImageRePass = document.querySelector('.eye-image-re-pass')



function hideShowSwicher(obj, image) {
    if (obj.type === 'password') {
        obj.type = 'text'
        image.src = '/static/images/eye/show.svg'
    } else {
        obj.type = 'password'
        image.src = '/static/images/eye/hide.svg'
    }
}







