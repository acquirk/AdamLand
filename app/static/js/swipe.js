document.addEventListener('DOMContentLoaded', (event) => {
    const inboxForm = document.getElementById('inboxForm');
    const inboxInput = document.getElementById('inboxInput');
    let touchstartY = 0;
    let touchendY = 0;

    function handleGesture() {
        if (touchendY < touchstartY) {
            // Swipe up detected
            if (inboxInput.value.trim() !== '') {
                inboxForm.submit();
            }
        }
    }

    inboxInput.addEventListener('touchstart', e => {
        touchstartY = e.changedTouches[0].screenY;
    });

    inboxInput.addEventListener('touchend', e => {
        touchendY = e.changedTouches[0].screenY;
        handleGesture();
    });
});
