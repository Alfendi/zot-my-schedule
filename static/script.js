function show() {
    document.getElementById('sidebar').classList.toggle('active');
  }

 $(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally
        var formData = $(this).serialize();  // Serialize the form data
        $.ajax({
            type: 'POST',
            url: '/submitted',
            data: formData,
            success: function(response) {
                // Update the content on the page
                $('#result').text(response.content);
            }
        });
    });
});