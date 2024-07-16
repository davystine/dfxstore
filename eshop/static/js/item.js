$(document).ready(function() {
    function updatePreview() {
        $('#item-name').text($('#id_name').val() || 'Item Name');
        $('#item-description').text($('#id_description').val() || 'Description');
        const price = $('#id_price').val() || '0';
        const salePrice = $('#id_sale_price').val() || '0';
        const onSale = $('#id_on_sale').is(':checked');

        if (onSale) {
            $('#sale-badge').show();
            $('#item-original-price').text('$' + price).show();
            $('#item-price').hide();
            $('#item-sale-price').text('$' + salePrice).show();
        } else {
            $('#sale-badge').hide();
            $('#item-original-price').hide();
            $('#item-price').text('$' + price).show();
            $('#item-sale-price').hide();
        }

        $('#item-units-in-stock').text('Units in Stock: ' + ($('#id_units_in_stock').val() || '0'));
    }

    $('#item-form input, #item-form select').on('input change', updatePreview);

    $('#id_image').on('change', function() {
        const fileInput = $(this)[0];
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            $('#item-image').attr('src', e.target.result);
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            $('#item-image').attr('src', '{% static "default-image.png" %}');
        }
    });

    $('#id_on_sale').on('change', function() {
        $('#sale-price-field').toggle($(this).is(':checked'));
        updatePreview();
    });

    updatePreview(); // Initial call to set up the preview



    // static/js/item.js

    $(document).ready(function() {
        $('#deleteModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget); // Button that triggered the modal
            var itemId = button.data('item-id'); // Extract info from data-* attributes
            var itemName = button.data('item-name');

            var modal = $(this);
            modal.find('.modal-body #itemName').text(itemName);
            modal.find('#delete-form').attr('action', '/management/items/delete/' + itemId + '/');
        });
    });
    
});
