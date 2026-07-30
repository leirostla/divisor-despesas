MVP significa **Minimum Viable Product**, em português, **Produto Mínimo Viável**.

É a primeira versão funcional de um sistema, contendo apenas os recursos essenciais para resolver o problema principal e permitir que o produto seja testado por usuários reais.

A ideia não é criar um sistema incompleto ou malfeito. A ideia é criar uma versão:

* simples;
* funcional;
* utilizável;
* rápida de desenvolver;
* suficiente para validar se a solução realmente é útil.

No caso do seu sistema de divisão de despesas, um MVP poderia ter apenas:

1. criação de um grupo;
2. cadastro das pessoas do grupo;
3. cadastro de despesas;
4. indicação de quem pagou;
5. indicação de quem participa da divisão;
6. cálculo do saldo de cada pessoa;
7. sugestão de quem deve pagar a quem.

Exemplo:

```text
Grupo: Viagem para Recife

Pessoas:
- Ana
- Bruno
- Carlos

Despesas:
- Hotel: R$ 600,00, pago por Ana
- Combustível: R$ 300,00, pago por Bruno
- Restaurante: R$ 150,00, pago por Carlos
```

O MVP calcula quanto cada um deveria ter pago e mostra algo como:

```text
Bruno deve pagar R$ 50,00 para Ana.
Carlos deve pagar R$ 200,00 para Ana.
```

Isso já resolve o problema principal do sistema.

Recursos que provavelmente não precisariam estar na primeira versão:

* login com Google;
* aplicativo para celular;
* notificações;
* envio de comprovantes;
* integração com bancos;
* suporte a várias moedas;
* gráficos;
* comentários nas despesas;
* parcelamento;
* exportação para PDF;
* divisão por porcentagem;
* divisão por cotas;
* modo offline.

Esses recursos podem ser adicionados depois, conforme o sistema seja testado.

A lógica do MVP é:

```text
problema principal
        ↓
menor conjunto de funcionalidades
        ↓
primeira versão utilizável
        ↓
teste com usuários
        ↓
melhorias
```

No seu projeto, o MVP serve também como estratégia de aprendizado. Em vez de tentar desenvolver imediatamente um sistema semelhante ao Splitwise completo, você começa com uma versão menor e aprende, aos poucos:

* Python;
* banco de dados;
* HTML e CSS;
* JavaScript;
* framework web;
* autenticação;
* regras de negócio;
* testes;
* publicação na internet.

Uma possível sequência seria:

**MVP 1:** programa Python no terminal que recebe os pagamentos e calcula os saldos.

**MVP 2:** aplicação web simples, sem login, com formulário para cadastrar pessoas e despesas.

**MVP 3:** aplicação com usuários, grupos e banco de dados.

**MVP 4:** histórico, edição de despesas e fechamento de contas.

**MVP 5:** notificações, comprovantes, gráficos e outros recursos.

Portanto, MVP não significa “versão definitiva”. Significa a menor versão que já entrega valor e permite verificar se a ideia funciona.

## Para o MVP, uma combinação coerente seria:
Django
Django ORM
SQLite
Templates do Django
HTML e CSS
Bootstrap opcional

## No seu projeto de divisão de despesas, uma possível stack seria
Python
Django
Django ORM
PostgreSQL
HTML
CSS
Bootstrap
JavaScript