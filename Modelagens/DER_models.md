# Diagrama Entidade-Relacionamento

Este diagrama representa as models atualmente declaradas em `app_divide/models`.
Os campos `id` são chaves primárias criadas implicitamente pelo Django.

```mermaid
erDiagram
    AUTH_USER {
        integer id PK
        string username
        string password
        string email
        string first_name
        string last_name
        boolean is_staff
        boolean is_active
        boolean is_superuser
        datetime last_login "nullable"
        datetime date_joined
    }

    GRUPO {
        integer id PK
        string nome "max_length=100"
        text descricao "nullable"
        datetime data_criacao "auto_now_add"
    }

    DESPESA {
        integer id PK
        integer grupo_id FK
        string descricao "max_length=255"
        text observacao "nullable"
        decimal valor_total "10,2"
        date data_despesa "auto_now_add"
        integer criador_id FK
    }

    PARTICIPANTE_GRUPO {
        integer id PK
        integer grupo_id FK
        integer usuario_id FK
        string nome "max_length=100, nullable"
        boolean ativo "default=true"
    }

    PARTICIPACAO_DESPESA {
        integer id PK
        integer despesa_id FK
        integer participante_id FK
        decimal valor_devido "10,2, default=0.00"
    }

    PAGAMENTO {
        integer id PK
        integer valor_despesa_id FK "nullable"
        integer participante_grupo_pagador_id FK "nullable"
        decimal valor_pago "10,2, default=0.00"
    }

    GRUPO ||--o{ DESPESA : "possui [CASCADE]"
    GRUPO ||--o{ PARTICIPANTE_GRUPO : "possui [CASCADE]"
    AUTH_USER ||--o{ PARTICIPANTE_GRUPO : "participa como [CASCADE]"
    PARTICIPANTE_GRUPO ||--o{ DESPESA : "cria [CASCADE]"
    DESPESA ||--o{ PARTICIPACAO_DESPESA : "é dividida em [CASCADE]"
    PARTICIPANTE_GRUPO ||--o{ PARTICIPACAO_DESPESA : "deve [CASCADE]"
    DESPESA o|--o{ PAGAMENTO : "recebe [SET_NULL]"
    PARTICIPANTE_GRUPO o|--o{ PAGAMENTO : "realiza [SET_NULL]"
```

## Leitura do modelo

- `ParticipanteGrupo` materializa a associação entre um usuário e um grupo e identifica o criador de cada despesa.
- `Despesa` não possui mais relacionamento direto com `AUTH_USER`; seu campo `criador` referencia `ParticipanteGrupo`.
- `ParticipacaoDespesa` materializa a divisão de uma despesa entre os participantes, registrando o valor devido por cada um.
- `Pagamento` referencia opcionalmente uma despesa e o participante pagador; se um deles for excluído, a respectiva chave estrangeira passa a `NULL`.
- As demais chaves estrangeiras usam exclusão em cascata.

## Observações

- `AUTH_USER` corresponde à model configurada em `settings.AUTH_USER_MODEL`. Na configuração atual, é a model padrão `django.contrib.auth.models.User` (tabela `auth_user`).
- As models não declaram restrições `UniqueConstraint`. Assim, no estado atual, o banco permite repetir a associação usuário/grupo e a associação participante/despesa.
- Os nomes físicos padrão das tabelas são `app_divide_grupo`, `app_divide_despesa`, `app_divide_participantegrupo`, `app_divide_participacaodespesa` e `app_divide_pagamento`.
