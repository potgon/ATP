$(document).ready(function() {
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });

    $('#loginForm').submit(function(event) {
        event.preventDefault();
        var formData = {
            username: $('#loginForm input[name="username"]').val(),
            password: $('#loginForm input[name="password"]').val()
        };

        $.ajax({
            url: '/login/', 
            type: 'POST',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                alert('Login successful!');
            },
            error: function(xhr) {
                alert('Login failed: ' + xhr.responseText);
            }
        });
    });

    $('#registerForm').submit(function(event) {
        event.preventDefault();
        var formData = {
            username: $('#registerForm input[name="username"]').val(),
            email: $('#registerForm input[name="email"]').val(),
            first_name: $('#registerForm input[name="first_name"]').val(),
            last_name: $('#registerForm input[name="last_name"]').val(),
            password: $('#registerForm input[name="password"]').val(),
            priority: $('#registerForm input[name="priority"]').is(":checked")
        };
  
        $.ajax({
            url: '/register/',
            type: 'POST',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    alert('Registration successful!');
                } else {
                    alert('Registration failed');
                    console.error('Registration failed')
                }
            },
            error: function(xhr) {
                alert('Registration failed: ' + xhr.responseText);
                console.error('Registration failed: '+ xhr.responseText)
            }
        });
    });
});
