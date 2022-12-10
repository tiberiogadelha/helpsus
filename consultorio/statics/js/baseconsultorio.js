function redirectTo(url) {
    switch (url) {
        case 'getAttendancesTriagem':
            window.location.href = '/triagem/getAttendances';
            break;
        default:
            window.location.href = '/triagem/';
        
    }

}

function getDatetime() {
    const date = new Date();
    const dateString = ("0" + date.getDate()).slice(-2) + "/" + ("0"+(date.getMonth()+1)).slice(-2) + "/" +
        date.getFullYear() + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2);
    document.getElementById("datetimebox").innerHTML = dateString;
}