// Exemplo de consumo do JSON em um front-end
async function fetchPedidos(clienteId) {
    try {
        const response = await fetch(`/api/pedidos?cliente_id=${clienteId}`); // Substitua pela URL da sua API
        const data = await response.json();

        if (data.length > 0) {
            console.log("Pedidos encontrados:", data);
            // Renderize os dados na interface do usuário
        } else {
            console.log("Nenhum pedido encontrado.");
        }
    } catch (error) {
        console.error("Erro ao buscar pedidos:", error);
    }
}

// Exemplo de uso
fetchPedidos(1); // Busca os pedidos do cliente com ID 1