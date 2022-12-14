function redirectTo(url) {
    switch (url) {
        case 'receptPatient':
            window.location.href = '/consultorio/visualizar-pacientes-pendentes';
            return;
            
        case 'createExamOrder':
            window.location.href = '/consultorio/solicitar-exame';
            return;
        case 'createPillOrder':
            window.location.href = '/consultorio/solicitar-medicamentos';
            return;
        case 'createSickNote':
            window.location.href = '/consultorio/emitir-atestado';
            return;
        default:
            window.location.href = '/consultorio/';
        
    }

}

function getDatetime() {
    const date = new Date();
    const dateString = ("0" + date.getDate()).slice(-2) + "/" + ("0"+(date.getMonth()+1)).slice(-2) + "/" +
        date.getFullYear() + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2);
    document.getElementById("datetimebox").innerHTML = dateString;
}
