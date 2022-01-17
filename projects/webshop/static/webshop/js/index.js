function logout_confirmation(event) {
    const choice = window.confirm("Da li ste sigurni da želite da se odjavite?")
    if (choice == false) {
        event.preventDefault();
        return false
    }
}
function delete_user_confirmation(event) {
    const choice = window.confirm("Da li ste sigurni da želite da obrišete nalog?")
    if (choice == false) {
        event.preventDefault();
        return false
    }
}
function delete_product_confirmation(event) {
    const choice = window.confirm("Da li ste sigurni da želite da obrišete ovaj proizvod?")
    if (choice == false) {
        event.preventDefault();
        return false
    }
}
