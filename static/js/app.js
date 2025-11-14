// Elementos do DOM
const formTeste = document.getElementById('formTeste');
const ipInput = document.getElementById('ip');
const portaInput = document.getElementById('porta');
const testesContainer = document.getElementById('testesContainer');
const btnAdicionarRegra = document.getElementById('btnAdicionarRegra');
const btnLimparTestes = document.getElementById('btnLimparTestes');
const modalRegra = document.getElementById('modalRegra');
const formRegra = document.getElementById('formRegra');
const btnCancelar = document.getElementById('btnCancelar');
const modalClose = document.querySelector('.modal-close');
const regrasTableBody = document.getElementById('regrasTableBody');
const modalTitle = document.getElementById('modalTitle');

let editandoIndex = null;

// Event Listeners
formTeste.addEventListener('submit', testarPacote);
btnAdicionarRegra.addEventListener('click', abrirModalAdicionar);
btnLimparTestes.addEventListener('click', limparTestes);
formRegra.addEventListener('submit', salvarRegra);
btnCancelar.addEventListener('click', fecharModal);
modalClose.addEventListener('click', fecharModal);

// Delegação de eventos para editar/deletar regras
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-edit')) {
        const row = e.target.closest('.regra-row');
        const index = row.dataset.index;
        abrirModalEditar(index);
    }
    if (e.target.classList.contains('btn-delete')) {
        const row = e.target.closest('.regra-row');
        const index = row.dataset.index;
        deletarRegra(index);
    }
});

// Fechar modal ao clicar fora
modalRegra.addEventListener('click', (e) => {
    if (e.target === modalRegra) {
        fecharModal();
    }
});

// Funções
async function testarPacote(e) {
    e.preventDefault();
    
    const ip = ipInput.value.trim();
    const porta = portaInput.value.trim();
    
    if (!ip || !porta) {
        alert('Por favor, preencha IP e Porta');
        return;
    }
    
    try {
        const response = await fetch('/api/testar-pacote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ip, porta })
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert('Erro: ' + (error.erro || 'Erro desconhecido'));
            return;
        }
        
        const resultado = await response.json();
        adicionarTesteAoHistorico(resultado);
        
        // Limpa o formulário
        formTeste.reset();
        ipInput.focus();
        
    } catch (error) {
        console.error('Erro ao testar pacote:', error);
        alert('Erro ao testar pacote');
    }
}

function adicionarTesteAoHistorico(teste) {
    const testeCard = document.createElement('div');
    testeCard.className = 'teste-card';
    
    let conectividadeHTML = '';
    if (teste.conectividade === null) {
        conectividadeHTML = '<span class="icon">⚠️</span> Host não encontrado';
    } else if (teste.conectividade) {
        conectividadeHTML = '<span class="icon">✓</span> Porta ABERTA';
    } else {
        conectividadeHTML = '<span class="icon">✗</span> Porta FECHADA';
    }
    
    const decisaoClass = teste.decisao === 'PERMITIDO' ? 'permitido' : 'bloqueado';
    const decisaoHTML = teste.decisao === 'PERMITIDO'
        ? '<span class="icon">✅</span> PERMITIDO'
        : '<span class="icon">❌</span> BLOQUEADO';
    
    testeCard.innerHTML = `
        <div class="teste-header">
            <span class="teste-ip">${teste.ip}:${teste.porta}</span>
            <span class="teste-servico">${teste.servico}</span>
            <span class="teste-timestamp">${teste.timestamp}</span>
        </div>
        <div class="teste-body">
            <div class="teste-conectividade">${conectividadeHTML}</div>
            <div class="teste-decisao ${decisaoClass}">${decisaoHTML}</div>
        </div>
    `;
    
    // Insere no início do container
    testesContainer.insertBefore(testeCard, testesContainer.firstChild);
    
    // Remove mensagem de vazio se existir
    const emptyMsg = testesContainer.querySelector('.empty-message');
    if (emptyMsg) {
        emptyMsg.remove();
    }
}

function abrirModalAdicionar() {
    editandoIndex = null;
    modalTitle.textContent = 'Adicionar Regra';
    formRegra.reset();
    document.getElementById('modalIp').disabled = false;
    document.getElementById('modalPorta').disabled = false;
    modalRegra.classList.add('active');
    document.getElementById('modalIp').focus();
}

function abrirModalEditar(index) {
    editandoIndex = index;
    modalTitle.textContent = 'Editar Regra';
    
    const row = document.querySelector(`[data-index="${index}"]`);
    const ip = row.querySelector('.ip').textContent;
    const porta = row.querySelector('.porta').textContent;
    const acao = row.querySelector('.badge').textContent.trim();
    const descricao = row.querySelector('.descricao').textContent;
    
    document.getElementById('modalIp').value = ip;
    document.getElementById('modalPorta').value = porta;
    document.getElementById('modalAcao').value = acao;
    document.getElementById('modalDescricao').value = descricao === '-' ? '' : descricao;
    
    // Desabilita IP e Porta ao editar
    document.getElementById('modalIp').disabled = true;
    document.getElementById('modalPorta').disabled = true;
    
    modalRegra.classList.add('active');
}

function fecharModal() {
    modalRegra.classList.remove('active');
    formRegra.reset();
    editandoIndex = null;
}

async function salvarRegra(e) {
    e.preventDefault();
    
    const ip = document.getElementById('modalIp').value.trim();
    const porta = document.getElementById('modalPorta').value.trim();
    const acao = document.getElementById('modalAcao').value;
    const descricao = document.getElementById('modalDescricao').value.trim();
    
    if (!ip || !porta || !acao) {
        alert('Por favor, preencha todos os campos obrigatórios');
        return;
    }
    
    try {
        let response;
        
        if (editandoIndex !== null) {
            // Editar
            response = await fetch(`/api/regras/${editandoIndex}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ acao, descricao })
            });
        } else {
            // Adicionar
            response = await fetch('/api/regras', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ip, porta, acao, descricao })
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            alert('Erro: ' + (error.erro || 'Erro desconhecido'));
            return;
        }
        
        fecharModal();
        location.reload(); // Recarrega a página para atualizar a tabela
        
    } catch (error) {
        console.error('Erro ao salvar regra:', error);
        alert('Erro ao salvar regra');
    }
}

async function deletarRegra(index) {
    if (!confirm('Tem certeza que deseja deletar esta regra?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/regras/${index}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert('Erro: ' + (error.erro || 'Erro desconhecido'));
            return;
        }
        
        location.reload(); // Recarrega a página
        
    } catch (error) {
        console.error('Erro ao deletar regra:', error);
        alert('Erro ao deletar regra');
    }
}

async function limparTestes() {
    if (!confirm('Tem certeza que deseja limpar o histórico de testes?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/testes', {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            alert('Erro ao limpar histórico');
            return;
        }
        
        testesContainer.innerHTML = '<p class="empty-message">Nenhum teste realizado ainda</p>';
        
    } catch (error) {
        console.error('Erro ao limpar testes:', error);
        alert('Erro ao limpar histórico');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    console.log('App carregado!');
});
