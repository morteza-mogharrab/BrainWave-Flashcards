$(document).ready(function(){
    // Check if there are elements with class 'memorizePanel'
    if ($('.memorizePanel').length != 0) {

        // Click event for flipping the card
        $('.flipCard').click(function(){
            if ($('.cardFront').is(":visible") == true) {
                $('.cardFront').hide();
                $('.cardBack').show();
            } else {
                $('.cardFront').show();
                $('.cardBack').hide();
            }
        });
    }

    // Check if there are elements with class 'cardForm'
    if ($('.cardForm').length != 0) {

        // Form submission event for trimming input values
        $('.cardForm').submit(function(){

            var frontTrim = $.trim($('#front').val());
            $('#front').val(frontTrim);
            var backTrim = $.trim($('#back').val());
            $('#back').val(backTrim);

            // Check if input fields are empty
            if (! $('#front').val() || ! $('#back').val()) {
                return false;
            }
        });
    }

    // Check if there are elements with class 'editPanel'
    if ($('.editPanel').length != 0) {

        // Function to check and handle radio button selection
        function checkit() {
            var checkedVal = $('input[name=type]:checked').val();
            if (checkedVal === undefined) {
                // hide the fields if no radio button is checked
                $('.fieldFront').hide();
                $('.fieldBack').hide();
                $('.saveButton').hide();
            } else {
                $('.toggleButton').removeClass('toggleSelected');
                $(this).addClass('toggleSelected');

                // Adjust textarea rows based on selected radio button
                if (checkedVal == '1') {
                    $('textarea[name=back]').attr('rows', 5);
                } else {
                    $('textarea[name=back]').attr('rows', 12);
                }

                // Show the fields and save button
                $('.fieldFront').show();
                $('.fieldBack').show();
                $('.saveButton').show();
            }
        }

        // Click event for radio button selection
        $('.toggleButton').click(checkit);

        // Check and handle radio button selection initially
        checkit();
    }

    // Attach FastClick to remove short delay on click for touch devices
    FastClick.attach(document.body);
});
