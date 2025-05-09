# 📈 Plano de Evolução – App Dindin

## 1. 🔄 Tela de Saldos/Contas (`SaldoView.swift`)

### 🎯 Objetivo:
Melhorar a usabilidade e a manipulação das contas existentes.

### ✅ Melhorias planejadas:
- [X] **Editar conta via swipe**
  - Adicionar botão de edição ao lado do botão de deletar (`swipeActions`).
  - Abrir a bottom sheet (`AddEditAccountView`) com a conta selecionada.
- [x] **Atualizar a lista após edição**
  - Garantir que ao fechar a edição, a conta seja atualizada na lista automaticamente.
- [ ] **Ordenar contas por nome ou saldo** (extra)
  - Adicionar opção de ordenação para facilitar visualização.

---

## 2. ➕ Tela de Nova Conta (`AddEditAccountView.swift`)

### 🎯 Objetivo:
Tornar o formulário mais amigável, visual e completo.

### ✅ Melhorias planejadas:
- [ ] **Foco automático no campo "Nome da conta"**
  - Usar `.focused()` para ativar o teclado no início.
- [ ] **Campo "Saldo" com máscara monetária**
  - Exibir valor formatado com separador de milhar e símbolo "R$".
  - Ex: `R$ 1.234,56`
- [ ] **Transformar campo de ícone em uma lista visual de ícones**
  - Substituir o `TextField` por um `LazyVGrid` com ícones predefinidos.
  - Permitir seleção visual com destaque do ícone escolhido.
- [ ] **Reduzir a altura da bottom sheet**
  - Usar `.presentationDetents([.medium, .large])` para um layout mais compacto.
- [ ] **Novo campo: "Titular"**
  - Adicionar botão de seleção entre "👨 Ricardo" e "👩 Priscila".
  - Internamente pode ser armazenado como `"ricardo"` ou `"priscila"`.
- [ ] **Novo campo: "Instituição"**
  - Adicionar seleção de ícones de bancos/instituições financeiras (pré-definidos).
  - Ex: `🏦 Nubank`, `🏦 Banco do Brasil`, `🏦 Inter`.

---

## 3. 📦 Estrutura de Dados (ajustes no modelo `Account`)

### ✅ Campos novos:
- [ ] `titular: String` (ex: `"ricardo"`, `"priscila"`)
- [ ] `instituicao: String` (ex: `"nubank"`, `"bb"`, `"inter"`)

---

## 4. 🧪 Testes e Validações

- [ ] Testar a criação de conta com todos os campos novos.
- [ ] Testar edição com atualização imediata na tela de saldos.
- [ ] Garantir persistência local (Realm) para os novos campos.

---

## 5. 🛠 Extras futuros

| Item | Prioridade | Observação |
|------|------------|------------|
| Sincronização com servidor | Alta | Implementar sincronismo entre banco local (Realm) e API |
| Backup/restore via iCloud | Média | Para segurança dos dados |
| Multiusuário com chave compartilhada | Média | Ex: "conta da família" acessada por Ricardo e Priscila |
| Estatísticas e gráficos | Média | Evolução de saldo, categorias etc |