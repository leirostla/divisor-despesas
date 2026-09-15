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

const groupModal = document.getElementById('groupModal');

if (groupModal) {
    const groupForm = groupModal.querySelector('form');
    const groupNameInput = groupModal.querySelector('[name="nome"]');

    groupModal.addEventListener('shown.bs.modal', () => groupNameInput?.focus());
    groupModal.addEventListener('hidden.bs.modal', () => groupForm?.reset());
}

const paymentModal = document.getElementById('paymentModal');

if (paymentModal) {
    const paymentForm = paymentModal.querySelector('[data-payment-form]');
    const expenseSelect = paymentModal.querySelector('[name="despesa"]');

    paymentModal.addEventListener('shown.bs.modal', () => expenseSelect?.focus());
    paymentModal.addEventListener('hidden.bs.modal', () => paymentForm?.reset());
}
