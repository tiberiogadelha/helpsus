function redirectTo(url) {
    switch (url) {
        case 'createPatient':
            window.location.href = '/recepcao/paciente';
            break;
        case 'editPatient':
            window.location.href = '/recepcao/editar-paciente';
            break;
        case 'newAttendance':
            window.location.href = '/recepcao/atendimento';
            break;
        case 'viewAttendances':
            window.location.href = '/recepcao/visualizarAtendimentos';
            break;
        default:
            window.location.href = '/recepcao/';
        
    }

}

function getDatetime() {
    const date = new Date();
    const dateString = ("0" + date.getDate()).slice(-2) + "/" + ("0"+(date.getMonth()+1)).slice(-2) + "/" +
        date.getFullYear() + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2);
    document.getElementById("datetimebox").innerHTML = dateString;
}