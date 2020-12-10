document.addEventListener('DOMContentLoaded', function() {

    // (1) Compute refinanced loan payments
    document.getElementById('form_compute_loan').onsubmit = function() {

        // Obtain and parse form data
        var payment_display = document.getElementById("payment_display"); 
        var amount = document.getElementById("amount").value;
        var period = document.getElementById("period").value;
        var IR_old = document.getElementById("IR_old").value;
        var frequency = document.getElementById("frequency").value;
        var start = document.getElementById("start").value;
        var num_payments = document.getElementById("num_payments").value;
        var last_payment = document.getElementById("last_payment").value;
        var next_payment = document.getElementById("next_payment").value;
        var IR_new = document.getElementById("IR_new").value;

        // Error catching in case of invalid form inputs
        if (amount.trim() == "") {
            alert("Error: You must indicate the original loan amount.");
            return false;
        } else if (period.trim() == "") {
            alert("Error: You must indicate the loan term/period.");
            return false;
        } else if (IR_old.trim() == "") {
            alert("Error: You must indicate the original interest rate.");
            return false;
        } else if (frequency == "None") {
            alert("Error: You must indicate the payment frequency.");
            return false;
        } else if (start == "None") {
            alert("Error: You must indicate when the first payment occurred.");
            return false;
        } else if (num_payments.trim() == "") {
            alert("Error: You must indicate the number of payments made so far.");
            return false;
        } else if (last_payment == "None") {
            alert("Error: You must indicate when the last payment occurred.");
            return false;
        } else if (next_payment == "None") {
            alert("Error: You must indicate when the next payment will occur.");
            return false;
        } else if (IR_new.trim() == "") {
            alert("Error: You must indicate the new interest rate.");
            return false;
        }
        
        // Compute new loan payment & display on screen
        var payment_old = compute_loan_old(amount, IR_old, period, start, frequency);
        var loan_outstanding = compute_loan_outstanding(amount, payment_old, IR_old, frequency, start, num_payments, last_payment);
        var payment_new = compute_loan_new(loan_outstanding, IR_new, frequency, next_payment, period * frequency - num_payments)
        payment_display.innerHTML = `New Monthly Payment: $${payment_new}`;  

        // Update hidden form field (if user wants to add loan to expenses list)
        document.getElementById("loan_amount").value = `${payment}`;
        return false;
    };

        // (2) Prompt user for loan name before adding it to list of expenses
        document.getElementById("form_add_loan").onsubmit = function() {
        var loan_name = prompt("Please enter a name for this loan.", "<Type loan name here>");

        if (loan_name == null || loan_name.trim() == "" || loan_name == "<Type loan name here>") {
            alert("You must enter a valid loan name.");
            return false;
        } else {
            document.getElementById("loan_name").value = `${loan_name}`;
        }
    };
});

// Computes the original loan payment amount
function compute_loan_old(amount, int_rate, period, start, frequency) {

    // Compute periodic interest rate & number of repayments
    i = (int_rate / 100) / frequency;
    n = period * frequency;

    // Compute annuity & corresponding payment amount
    annuity_PV = ((1 - Math.pow((1 + i), -n)) / i);
        
    if (start == "deferred") {
        annuity_PV *= (1 + i);
    }

    payment = (amount / annuity_PV).toFixed(2);
    return payment;
};

// Computes the current outstanding loan balance (after `num_payments` payments)
function compute_loan_outstanding(loan_original, payment, int_rate, frequency, start, num_payments, last_payment) {
    
    // Compute periodic interest rate & equivalent monthly interest rate
    i = (int_rate / 100) / frequency;
    i_monthly = Math.pow((1 + i), frequency / 12) - 1;

    // Compute present value of original loan amount
    loan_original *= Math.pow((1 + i), num_payments);
    loan_original *= Math.pow((1 + i_monthly), last_payment);
    
    // Compute present value of the loan repayments made so far
    annuity_PV = payment * (Math.pow((1 + i), num_payments) - 1) / i;
    annuity_PV *= Math.pow((1 + i_monthly), last_payment)

    if (start == "deferred") {
        loan_original *= (1 + i);
        annuity_PV *= (1 + i);
    }

    // Return outstanding loan balance
    return loan_original - annuity_PV;
}

// Compute new loan payment amount
function compute_loan_new(amount, int_rate, frequency, next_payment, remaining_payments) {

    // Compute periodic int. rate, equivalent monthly int. rate, and # payments to go
    i = (int_rate / 100) / frequency;
    i_monthly = Math.pow((1 + i), frequency / 12) - 1;
    n = remaining_payments;

    // Compute outstanding loan balance one period before the first new payment commences
    scale_factor = Math.pow((1 + i_monthly), next_payment) * Math.pow((1 + i), -1);
    amount *= scale_factor;
    
    // Compute annuity, new payment amount, & return new amount
    annuity_PV = (1 - Math.pow((1 + i), -n)) / i;
    payment = (amount / annuity_PV).toFixed(2);
    return payment;
};