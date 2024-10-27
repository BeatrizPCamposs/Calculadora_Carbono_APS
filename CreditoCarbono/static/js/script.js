function calcularEmissoes() {
    // Verificar se o formulário é válido
    if (validarFormulario()) {
        // Mostrar a seção 8
        document.getElementById('secao8').style.display = 'block';

        // Opcional: rolar para a seção 8
        document.getElementById('secao8').scrollIntoView({ behavior: 'smooth' });
    }
}

function validarFormulario() {
    const nome = document.getElementById("nomeUser").value;
    const estado = document.getElementById("selectRegiao").value;
    const consumoKwh = document.getElementById("consumo_kwh").value;
    const valorReais = document.getElementById("valor_reais").value;
    const residuosGerados = document.getElementById("residuos_gerados").value;
    const consumoCarne = document.getElementById("consumo_carne").value;

    if (!nome) {
        alert("Por favor, preencha seu nome.");
        return false;
    }

    if (estado === "Selecione") {
        alert("Por favor, selecione seu estado.");
        return false;
    }

    if (!consumoKwh && !valorReais) {
        alert("Por favor, informe o consumo de eletricidade ou o valor em reais.");
        return false;
    }

    if (!residuosGerados) {
        alert("Por favor, informe a quantidade de resíduos gerados.");
        return false;
    }

    if (!consumoCarne) {
        alert("Por favor, informe a quantidade de carne consumida.");
        return false;
    }

    return true; // Permite o envio do formulário
}
