function redirectAttendance(url, param) {
    console.log(url);
    console.log(param);
   
    switch (url) {
        case 'receptPatient':
            window.location.href = '/consultorio/visualizar-pacientes-pendentes';
            return;
            
        case 'createExamOrder':
            window.location.href = '/consultorio/solicitar-exame';
            return;
        case 'createPillOrder':
            window.open(`/consultorio/solicitar-medicamentos?attendance_data=${param}`);
            return;
        case 'createSickNote':
            window.open(`/consultorio/emitir-atestado?attendance_id=${param}`);
            return;
        case 'viewHistory':
            window.open(`/consultorio/visualizar-historico-paciente?patient=${param}`);
            return;

        case 'finishAttendance':
            window.open(`/consultorio/finalizar-atendimento?id=${param}`);
            return;
        default:
            return;
        
    }

}