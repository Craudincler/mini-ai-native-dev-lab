// Endereço da API (backend FastAPI rodando no Docker)
const API_URL = "http://localhost:8000";

// Elementos da página (os IDs vêm do index.html)
const loadButton = document.getElementById("load-demands-btn");
const statusBox = document.getElementById("status-box");
const demandList = document.getElementById("demand-list");
const summaryBox = document.getElementById("summary-box");
const demandForm = document.getElementById("demand-form");

// Busca todas as demandas (GET /demands) e mostra na lista
async function loadDemands() {
  statusBox.textContent = "Carregando dados da API...";
  demandList.innerHTML = "";

  try {
    const response = await fetch(`${API_URL}/demands`);
    const data = await response.json();
    const demands = data.demands;

    if (!demands || demands.length === 0) {
      statusBox.textContent = "Nenhuma demanda foi encontrada.";
      return;
    }

    statusBox.textContent = `Foram carregadas ${demands.length} demandas.`;

    demands.forEach((demand) => {
      const item = document.createElement("li");

      // Texto da demanda
      const text = document.createElement("span");
      text.textContent =
        `${demand.title} - ${demand.category} - ${demand.status} ` +
        `(responsável: ${demand.owner})`;

      // Botão de excluir: cada um sabe o id da sua demanda
      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.className = "delete-btn";
      deleteButton.textContent = "Excluir";
      deleteButton.addEventListener("click", () => {
        deleteDemand(demand.id, demand.title);
      });

      item.appendChild(text);
      item.appendChild(deleteButton);
      demandList.appendChild(item);
    });

    // Sempre que a lista é carregada, o resumo também é atualizado
    loadSummary();
  } catch (error) {
    statusBox.textContent =
      "Erro ao acessar a API. Verifique se os containers estão ativos.";
    console.error(error);
  }
}

// Busca o resumo por status (GET /summary) e mostra no card "Resumo"
async function loadSummary() {
  try {
    const response = await fetch(`${API_URL}/summary`);
    const summary = await response.json();

    summaryBox.textContent =
      `Total: ${summary.total} | ` +
      `Pendentes: ${summary.pending} | ` +
      `Em andamento: ${summary.in_progress} | ` +
      `Concluídas: ${summary.done}`;
  } catch (error) {
    summaryBox.textContent = "Não foi possível carregar o resumo.";
    console.error(error);
  }
}

// Envia o formulário para a API (POST /demands)
async function createDemand(event) {
  // Impede o navegador de recarregar a página ao enviar o formulário
  event.preventDefault();

  // Monta o objeto com os campos do formulário
  const newDemand = {
    title: document.getElementById("title").value,
    category: document.getElementById("category").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
    owner: document.getElementById("owner").value,
    created_at: document.getElementById("created_at").value,
  };

  try {
    const response = await fetch(`${API_URL}/demands`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newDemand),
    });

    if (!response.ok) {
      statusBox.textContent = "A API recusou os dados. Confira os campos.";
      return;
    }

    demandForm.reset();
    await loadDemands();
    statusBox.textContent = "Demanda salva com sucesso!";
  } catch (error) {
    statusBox.textContent =
      "Erro ao salvar. Verifique se os containers estão ativos.";
    console.error(error);
  }
}

// Exclui uma demanda pelo id (DELETE /demands/{id})
async function deleteDemand(id, title) {
  // Pede confirmação antes de apagar, porque não dá para desfazer
  const confirmed = confirm(`Excluir a demanda "${title}"?`);
  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/demands/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      statusBox.textContent = "Não foi possível excluir. A demanda pode já ter sido removida.";
      return;
    }

    await loadDemands();
    statusBox.textContent = "Demanda excluída com sucesso!";
  } catch (error) {
    statusBox.textContent =
      "Erro ao excluir. Verifique se os containers estão ativos.";
    console.error(error);
  }
}

// Liga os eventos aos elementos da página
loadButton.addEventListener("click", loadDemands);
demandForm.addEventListener("submit", createDemand);
