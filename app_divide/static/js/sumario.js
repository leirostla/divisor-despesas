const expenseModal = document.querySelector('[data-expense-modal]');
const openExpenseButton = document.querySelector('[data-open-expense-modal]');
const closeExpenseButtons = document.querySelectorAll('[data-close-expense-modal]');

if (expenseModal) {
    openExpenseButton?.addEventListener('click', () => expenseModal.showModal());
    closeExpenseButtons.forEach((button) => {
        button.addEventListener('click', () => expenseModal.close());
    });
    expenseModal.addEventListener('click', (event) => {
        if (event.target === expenseModal) expenseModal.close();
    });
    if (expenseModal.hasAttribute('data-has-errors')) expenseModal.showModal();
}
