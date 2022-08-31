function showButton() {
    const checked = document.getElementById('confirm').checked;

    if (checked)
        document.getElementById('btnNewAttendance').style.visibility = 'visible';
    else
        document.getElementById('btnNewAttendance').style.visibility = 'hidden';
}

function updateHour() {
    const now = Date.now();
    const date = new Date(now);
    const div = document.getElementById('attendanceHour');
    if (div) {
        div.value = date.toLocaleDateString() + ' às ' + date.toLocaleTimeString().slice(0,5);
    }
}      



function backToHome() {
    window.location.href = '/recepcao/';
}

