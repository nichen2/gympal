$(document).ready(function() {
    // Toggle between showing and hiding exercise details
    $('.toggle-details').click(function() {
        const cardBody = $(this).closest('.card-body');
        const details = cardBody.find('.exercise-details');
        const summary = cardBody.find('.exercise-default');

        // Check if the details are currently hidden
        if (details.hasClass('d-none')) {
            details.removeClass('d-none');
            summary.addClass('d-none');
            $(this).text('Hide Details'); 
        } else {
            details.addClass('d-none');
            summary.removeClass('d-none');
            cardBody.find('.toggle-details').first().text('View Details');
        }
    });

    // Toggle visibility of muscle group tags on click
    $('#group-by').click(function() {
        const muscleGroups = $('#muscle-group-tags');
        if (muscleGroups.hasClass('d-none')) {
            muscleGroups.removeClass('d-none');
        }
        else {
            muscleGroups.addClass('d-none');
        }
    });
});

// Handle exercise search functionality
$(document).ready(function() {
    $('#search-input').on('input', function() {
        const query = $(this).val();

        // Only search if the query has 2 or more characters
        if (query.length < 2) {
            $('#search-suggestions').empty().hide();
            return; 
        }

        // Perform an AJAX request to the search endpoint
        $.ajax({
            url: "/exercises/searchbar",
            type: "GET",
            data: { q: query },
            success: function(data) {
                $('#search-suggestions').empty().show();
                if (data.length === 0) {
                    $('#search-suggestions').append($('<a href="#" class="list-group-item list-group-item-action">No results</a>'));
                } else {
                    data.forEach(function(item) {
                        const suggestionItem = $('<a href="/exercises/show/' + item.id + '" class="list-group-item list-group-item-action">' + item.name + '</a>');
                        $('#search-suggestions').append(suggestionItem);
                    });
                }
            }
        });
    });

    // Close the search suggestions when clicking outside the search form
    $(document).on('click', function (e) {
        if (!$(e.target).closest('#search-form').length) {
            $('#search-suggestions').hide();
        }
    });
});
