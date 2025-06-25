function showNumberRange() {
    // Get the HTML element with the ID "this_div"
    const Div = document.getElementById("this_div");
    for (let i = 0; i < 15; i++) {
        // Append the current number and a line break to the inner HTML of the Div
        Div.innerHTML += i + '<br><br>';
    }
}
// Call the function to execute the number display
showNumberRange()