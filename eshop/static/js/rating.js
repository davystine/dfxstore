$(document).ready(function () {
    // Get form elements
    var $ratingForm = $('#rating-form');
    var $ratingStars = $('#average-rating-stars i');
    var rateItemUrl = $('#rate-item-url').val();
    var csrfToken = $('#csrf-token').val();

    // Update stars based on the average rating
    function updateStars(rating) {
        var fullStars = Math.floor(rating);
        var halfStar = rating % 1 >= 0.5;

        $ratingStars.each(function (index) {
            if (index < fullStars) {
                $(this).removeClass('bi-star').addClass('bi-star-fill');
            } else if (index === fullStars && halfStar) {
                $(this).removeClass('bi-star').addClass('bi-star-half');
            } else {
                $(this).removeClass('bi-star-fill').addClass('bi-star');
            }
        });
    }

    // On document ready, update the average rating stars
    var averageRating = parseFloat($('#average-rating-text').text());
    updateStars(averageRating);
});
