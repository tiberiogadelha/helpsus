function redirectTo(url, param) {
    switch (url) {
        case 'createExam':
            window.location.href = '/laboratorio/criar-exame';
            return;
        case 'editExams':
            window.location.href = `/laboratorio/view-exames`;
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