$(document).ready(function() {
    // Add item to cart event handler
    $(document).on('click', '#add-cart', function(e) {
        e.preventDefault();
        var itemId = $(this).val(); // Get item ID from the clicked button
        var itemQty = $('#item-qty').val(); // Get the latest value of item quantity

        $.ajax({
            type: 'POST',
            url: cartAddUrl,
            data: { 
                item_id: itemId,
                item_qty: itemQty,
                csrfmiddlewaretoken: csrfToken, 
                action: 'post'
            },
            success: function(json) {
                console.log('Add to cart success:', json);  // Debug line
                // Update cart quantity indicator
                $('#cart_quantity').text(json.qty);

                // Update units in stock display
                $('#units-in-stock').text(json.updated_stock);

                // Update max attribute of quantity input
                $('#item-qty').attr('max', json.updated_stock);

                // Reset quantity input to 1
                $('#item-qty').val(1);
            },
            error: function(xhr, errmsg, err) {  
                console.log('Add to cart error:', errmsg);  // Debug line
                alert('Error adding item to cart: ' + errmsg);
            }
        });
    });

    // Change event handler for quantity update
    $(document).on('change', '.update-cart', function() {
        var itemId = $(this).data('itemid');
        var newQty = $(this).val();
        var maxQty = parseInt($(this).attr('max'));

        if (newQty > maxQty) {
            $(this).val(maxQty);
            newQty = maxQty;
        }

        // AJAX call to update cart
        $.ajax({
            type: 'POST',
            url: cartUpdateUrl,
            data: { 
                item_id: itemId,
                item_qty: newQty,
                csrfmiddlewaretoken: csrfToken,
                action: 'post'
            },
            success: function(response) {
                console.log('Update cart success:', response);  // Debug line
                // Update cart quantity indicator
                $('#cart_quantity').text(response.qty);

                if (response.units_in_stock !== undefined) {
                    $('#' + itemId).siblings('.text-muted').text('Units in Stock: ' + response.units_in_stock);
                } else if (response.delete_confirmation) {
                    $('#deleteItemName').text(response.item_name);
                    $('#deleteConfirmationModal').modal('show');
                    $('#confirmDeleteBtn').data('itemid', itemId);
                }

                // Update the total in the HTML
                if (response.updated_total !== undefined) {
                    $('#cart-total').text('Total: $' + parseFloat(response.updated_total).toFixed(2));
                }
            },
            error: function(xhr, errmsg, err) {
                console.log('Update cart error:', errmsg);  // Debug line
                alert('Error updating cart: ' + errmsg);
            }
        });
    });

    // Click event handler for confirm delete button
    $('#confirmDeleteBtn').on('click', function() {
        var itemId = $(this).data('itemid');
        console.log("Confirm delete clicked for item ID:", itemId);  // Logging for debugging

        $.ajax({
            type: 'POST',
            url: cartDeleteUrl,
            data: {
                item_id: itemId,
                csrfmiddlewaretoken: csrfToken,
                action: 'delete'
            },
            success: function(response) {
                console.log('Delete cart success:', response);  // Debug line
                if (response.success) {
                    $('#deleteConfirmationModal').modal('hide');
                    location.reload();  // Optionally reload the page after successful deletion
                } else {
                    alert('Failed to delete item from cart.');
                }
            },
            error: function(xhr, errmsg, err) {
                console.log('Delete cart error:', errmsg);  // Debug line
                alert('Error deleting item from cart: ' + errmsg);
            }
        });
    });

    // Event handler for modal close to revert the quantity input
    $('#deleteConfirmationModal').on('hidden.bs.modal', function(e) {
        var itemId = $('#confirmDeleteBtn').data('itemid');
        console.log("Modal hidden, revert quantity for item ID:", itemId);  // Logging for debugging
        // Reset the quantity in the UI
        $('#' + itemId).val(1);
    });
});
