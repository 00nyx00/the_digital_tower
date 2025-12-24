// send values of clicked items

document.querySelectorAll('.scoreable').forEach(element => {
    element.addEventListener('click', function() {
        // 1. Get the value (e.g., 'test_good' or 'test_bad')
        let val = this.getAttribute('data-value');

        // 2. Send it to your /save route
        fetch('/save', {
            method: 'POST',
            body: new URLSearchParams({'value': val})
        });
        
        // No .then() block means the UI remains exactly as it is.
    });
});