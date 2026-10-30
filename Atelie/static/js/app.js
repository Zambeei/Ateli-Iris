// O JavaScript roda no NAVEGADOR, depois que o Flask entrega este HTML.

    // ENCONTRO 1: botão e GET. O navegador pede os alunos à API Python.
    document.querySelector('#buscar').addEventListener('click', async () => {
      // querySelector encontra um elemento pelo seu id (#).
      const lista = document.querySelector('#lista');
      const aviso = document.querySelector('#aviso');
      lista.replaceChildren(); 
      aviso.textContent = 'Consultando...'; 

      try {
        const resposta = await fetch('/api/cliente'); 
        const clientes = await resposta.json(); 
        if (!resposta.ok) throw new Error(clientes.erro); // 

        for (const c of clientes) { 
          const item = document.createElement('li'); // Cria <li>.
          item.textContent = `${c.cliente_id} - ${c.nome}`;
          lista.append(item); // Coloca o <li> dentro do <ul>.
        }
        aviso.textContent = `${clientes.length} cliente(s) exibido(s).`;
      } catch (erro) { // Falha de rede ou erro informado pelo Flask.
        aviso.textContent = `Falha: ${erro.message}`;
      }
    });

    // ENCONTRO 2: formulário e POST. O navegador envia JSON ao Python.
    document.querySelector('#cadastro').addEventListener('submit', async (evento) => {
      evento.preventDefault(); // Impede o recarregamento tradicional.
      const formulario = evento.currentTarget; // Formulário enviado.
      const aviso = document.querySelector('#cadastro-aviso');

      // .value lê o texto digitado; trim remove espaços das extremidades.
      const nome = document.querySelector('#nome').value.trim();
      const email = document.querySelector('#email').value.trim();
      const telefone = document.querySelector('#telefone').value.trim();
      const cpf = document.querySelector('#cpf').value.trim();
      const cliente = { nome: nome, email: email, telefone: telefone, cpf: cpf};
      aviso.textContent = 'Cadastrando...';

      try {
        const resposta = await fetch('/api/cliente', {
          method: 'POST', // Método HTTP para criar um aluno.
          headers: { 'Content-Type': 'application/json' }, // Formato.
          body: JSON.stringify(cliente) // Converte objeto JS em texto JSON.
        });
        const dados = await resposta.json(); // Lê o JSON da resposta.
        if (!resposta.ok) throw new Error(dados.erro); // 400, 409 ou 503.
        aviso.textContent = `Cliente ${dados.nome} cadastrado com ID ${dados.cliente_id}.`;
        formulario.reset(); // Limpa os campos.
        document.querySelector('#buscar').click(); // Atualiza a lista.
      } catch (erro) {
        aviso.textContent = `Falha: ${erro.message}`;
      }
    });