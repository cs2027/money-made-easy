document.addEventListener('DOMContentLoaded', function() {

    // (1) Compute loan payments based on user inputs (principal, int. rate, etc.)
    document.getElementById("form_compute_loan").onsubmit = function() {

        // Once form is submitted, parse information about loan
        var payment_display = document.getElementById("payment_display"); 
        var amount = document.getElementById("amount").value;
        var int_rate = document.getElementById("int_rate").value;
        var period = document.getElementById("period").value;
        var start = document.getElementById("start").value;
        var frequency = document.getElementById("frequency").value;

        // Error catching in case of invalid form inputs
        if (amount.trim() == "") {
            alert("Error: You must indicate the loan amount (principal).");
            return false;
        } else if (int_rate.trim() == "") {
            alert("Error: You must indicate the interest rate.");
            return false;
        } else if (period.trim() == "") {
            alert("Error: You must indicate the loan term/period.");
            return false;
        } else if (start == "None") {
            alert("Error: You must indicate when the first payment occurred.");
            return false;
        } else if (frequency == "None") {
            alert("Error: You must indicate the frequency of payments.");
            return false;
        }

        // Compute the loan repayment amount, display on screen
        var payment = compute_loan(amount, int_rate, period, start, frequency);
        payment_display.innerHTML = `Monthly Payment: $${payment}`;

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

// Helper function to compute payment amount for a loan
function compute_loan(amount, int_rate, period, start, frequency) {

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