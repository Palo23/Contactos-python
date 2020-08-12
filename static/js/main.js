const btns = document.querySelectorAll('.btn-delete')

if (btns) {
    const btnArray = Array.from(btns);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Estás seguro de eliminar?')) {
                e.preventDefault();
            }
        });
    });
}