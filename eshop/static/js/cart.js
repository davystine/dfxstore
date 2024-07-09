$(document).ready(function() {
    // Add item to cart event handler
    $(document).on('click', '#add-cart', function(e){
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
            success: function(json){
                // Update cart quantity indicator
                document.getElementById("cart_quantity").textContent = json.qty;

                // Update units in stock display
                $('#units-in-stock').text(json.updated_stock);

                // Update max attribute of quantity input
                $('#item-qty').attr('max', json.updated_stock);

                // Reset quantity input to 1
                $('#item-qty').val(1);
            },
            error: function(xhr, errmsg, err){  
                console.log(errmsg);
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
                if (response.units_in_stock !== undefined) {
                    $('#' + itemId).siblings('.text-muted').text('Units in Stock: ' + response.units_in_stock);
                } else if (response.delete_confirmation) {
                    $('#deleteItemName').text(response.item_name);
                    $('#deleteConfirmationModal').modal('show');
                    $('#confirmDeleteBtn').data('itemid', itemId);
                } else {
                    alert('Failed to update cart.');
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
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
                if (response.success) {
                    $('#deleteConfirmationModal').modal('hide');
                    location.reload();  // Optionally reload the page after successful deletion
                } else {
                    alert('Failed to delete item from cart.');
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
                alert('Error deleting item from cart: ' + errmsg);
            }
        });
    });

    // Event handler for modal close to revert the quantity input
    $('#deleteConfirmationModal').on('hidden.bs.modal', function (e) {
        var itemId = $('#confirmDeleteBtn').data('itemid');
        console.log("Modal hidden, revert quantity for item ID:", itemId);  // Logging for debugging
        // Reset the quantity in the UI
        $('#' + itemId).val(1);

        //Reverting the UI state only, not updating the server
    });
});
