const btn = document.querySelector('.btn')
const modalOverlay = document.querySelector('.modal-overlay')
const modal = document.querySelector('.modal')
const butt = document.querySelector('.butt')

btn.addEventListener('dblclick', (el) => {
    let path = el.currentTarget.getAttribute('data-path')

    modal.classList.remove('modal--visible')

    document.querySelector(`[data-target="${path}"]`).classList.add('modal--visible')
    modalOverlay.classList.add('modal-overlay--visible')
})

modalOverlay.addEventListener('click', (el) => {
    if (el.target == modalOverlay || el.target == butt) {
        modalOverlay.classList.remove('modal-overlay--visible')
        modal.classList.remove('modal--visible')
    }
})