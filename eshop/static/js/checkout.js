$(document).ready(function() {
    const $shippingForm = $('#shippingForm');
    const $proceedButton = $('#proceedToPayment');
    const $clearCartForm = $('#clearCartForm');

    function validateForm() {
        const isValid = $shippingForm[0].checkValidity();
        $proceedButton.prop('disabled', !isValid);
    }

    function handleRedirection() {
        if ($proceedButton.prop('disabled') === false) {
            $clearCartForm.submit();
        }
    }

    $shippingForm.on('input change', validateForm);
    validateForm();  // Initial validation

    $proceedButton.on('click', handleRedirection);
});
