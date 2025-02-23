// Immediately Invoked Function Expression (IIFE) to encapsulate the code
(function() {
    console.log("hello");
    return 1;
}());

// Another IIFE to handle text selection and open a new window
(function() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        const queryParam = encodeURIComponent(selectedText);
        const appUrl = `http://localhost:8501?q=${queryParam}`;
        window.open(appUrl, '_blank');
    } else {
        console.warn("No text selected.");
    }
}());
