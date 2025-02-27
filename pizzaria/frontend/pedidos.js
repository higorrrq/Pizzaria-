document.getElementById('clienteForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Impede o envio do formulário

    const clienteId = document.getElementById('clienteId').value;
    const resultadoDiv = document.getElementById('resultado');

    // Limpa resultados anteriores
    resultadoDiv.innerHTML = '';

    try {
        // Faz a requisição à API
        const response = await fetch(`http://127.0.0.1:8000/api/pedidos?cliente_id=${clienteId}`);
        const data = await response.json();
        console.log(response)
        if (data.length > 0) {
            // Exibe os pedidos
            data.forEach(pedido => {
                const pedidoDiv = document.createElement('div');
                pedidoDiv.classList.add('pedido');

                pedidoDiv.innerHTML = `
                    <h3>Pedido ID: ${pedido.PedidoID}</h3>
                    <p><strong>Data:</strong> ${pedido.DataPedido}</p>
                    <p><strong>Status:</strong> ${pedido.Status}</p>
                    <p><strong>Total:</strong> R$ ${Number(pedido.Total).toFixed(2)}</p>
                    <p><strong>Cliente:</strong> ${pedido.Cliente}</p>
                `;

                resultadoDiv.appendChild(pedidoDiv);
            });
        } else {
            resultadoDiv.innerHTML = '<p>Nenhum pedido encontrado para este cliente.</p>';
        }
    } catch (error) {
        console.error('Erro ao buscar pedidos:', error);
        resultadoDiv.innerHTML = '<p>Erro ao buscar pedidos. Tente novamente mais tarde.</p>';
    }
});