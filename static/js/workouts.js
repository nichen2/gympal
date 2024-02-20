// Function to perform the search and filtering
function searchAndFilterExercises() {
    const query = $('#exercises-search').val();
    const muscleGroup = $('#muscle-group-filter').val();

    if (query.length < 1 && muscleGroup === '') {
        $('#exercises-results').empty().hide();
        return;
    }

    $.ajax({
        url: "/workouts/search",
        type: "GET",
        data: { q: query, m: muscleGroup },
        success: function(data) {
            $('#exercises-results').empty().show();
            if (data.length === 0) {
                $('#exercises-results').append($('<li class="list-group-item">No results found</li>'));
            } else {
                data.forEach(function(item) {
                    const exerciseItem = $(`<li class="list-group-item d-flex justify-content-between align-items-center">${item.name}<button class="btn btn-primary btn-sm add-exercise" data-id="${item.id}" data-name="${item.name}">Add to workout</button></li>`);
                    $('#exercises-results').append(exerciseItem);
                });
            }
        }
    });
}

// Document ready function
$(document).ready(function() {
    // Attach event listener for search and filter inputs
    $('#exercises-search, #muscle-group-filter').on('input change', searchAndFilterExercises);

    // Event listener for adding exercise to draft
    $('#exercises-results').on('click', '.add-exercise', function() {
        const exerciseName = $(this).data('name');
        const exerciseId = $(this).data('id');
        
        const draftItem = $(`<li class="list-group-item d-flex justify-content-between align-items-center workout-exercise" data-id="${exerciseId}">
            ${exerciseName}
            <div>
                Sets: <input type="number" min="1" class="form-control sets" style="width: auto; margin-right: 10px;" placeholder="Sets">
                Reps: <input type="number" min="1" class="form-control reps" style="width: auto;" placeholder="Reps">
                <button class="btn btn-danger btn-sm remove-exercise">Remove</button>
            </div>
        </li>`);
        $('#workout-list').append(draftItem);
    });

    // Event listener for removing an exercise from the draft
    $('#workout-list').on('click', '.remove-exercise', function() {
        $(this).closest('li').remove();
    });

    // Event listener for saving workouts to DB
    $('#save-workout').click(function() {
        console.log("saving workout");
        const workoutName = $('#workout-name').val();
        const exercises = [];
        $('.workout-exercise').each(function() {
            const exerciseId = $(this).data('id');
            console.log(exerciseId);
            const sets = $(this).find('.sets').val();
            const reps = $(this).find('.reps').val();
            exercises.push({
                exerciseId,
                sets,
                reps
            });
        });
        const workoutData = {
            name: workoutName,
            exercises: exercises
        }

        // AJAX request to send workoutData to the server
        $.ajax({
            type: 'POST',
            url: '/workouts/save_workout',
            contentType: 'application/json',
            data: JSON.stringify(workoutData),
            success: function(response) {
                
                alert('Workout saved successfully!');
            },
            error: function(error) {
                // Handle error
                console.error('Error saving workout:', error);
                alert('Error saving workout. Please try again.');
            }
        });
    });
});
