// main.js

document.addEventListener('DOMContentLoaded', (event) => {
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Function to add a new project
    window.addProject = function(event, bucketId) {
        event.preventDefault();
        const input = event.target.querySelector('input');
        const projectName = input.value.trim();
        if (projectName) {
            fetch('/add_project', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ bucket_id: bucketId, project_name: projectName }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error adding project: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the project.');
            });
        }
        input.value = '';
    };

    // Function to add a new goal
    window.addGoal = function(event, projectId) {
        event.preventDefault();
        const input = event.target.querySelector('input');
        const goalDescription = input.value.trim();
        if (goalDescription) {
            fetch('/add_goal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ project_id: projectId, goal_description: goalDescription }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error adding goal: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the goal.');
            });
        }
        input.value = '';
    };

    // Flash message close functionality
    var closeButtons = document.querySelectorAll('.alert .close');
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            var alert = this.closest('.alert');
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300);
        });
    });
});
