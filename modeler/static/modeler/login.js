const logOutForm = document.getElementById("log-out-form");

if (logOutForm) {
    document.getElementById("log-out").onclick = function() {
        logOutForm.submit();
    }
}