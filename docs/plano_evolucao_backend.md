# Plano de Evolução do Backend DinDin

## 1. Fundação e Qualidade
- [ ] **Testes Automatizados**
  - Cobertura de testes unitários para Lambdas principais
  - Testes de integração (ex: simular upload de OFX e consulta de transações)
- [ ] **CI/CD**
  - Pipeline automatizado para rodar testes, lint e deploy (GitHub Actions, GitLab CI, etc)
- [ ] **Documentação**
  - Manter OpenAPI sempre atualizada
  - Wiki ou docs para onboarding de novos devs

---

## 2. Funcionalidades Essenciais
- [ ] **Autenticação e Autorização**
  - Integração com Cognito, Auth0 ou JWT customizado
  - Permitir múltiplos usuários, cada um com seus próprios dados
- [ ] **Multi-conta e Multi-arquivo**
  - Permitir upload de múltiplos arquivos OFX por usuário/conta
  - Histórico de uploads e seleção de extrato para análise
- [ ] **Categorias Inteligentes**
  - Classificação automática de transações por categoria (machine learning ou regras)
  - Edição manual de categorias pelo usuário

---

## 3. APIs e Integrações
- [ ] **Endpoints Avançados**
  - API para dashboard financeiro (resumos, gráficos, evolução de saldo)
  - API para exportação de dados (CSV, PDF)
- [ ] **Webhooks e Notificações**
  - Notificações por e-mail/push para eventos importantes (ex: novo extrato, saldo baixo)
- [ ] **Integração com outros bancos**
  - Suporte a outros formatos além de OFX (ex: CNAB, CSV de bancos digitais)

---

## 4. Escalabilidade e Performance
- [ ] **Monitoramento e Logs**
  - Integração com CloudWatch, Sentry ou Datadog
  - Alertas para falhas e lentidão
- [ ] **Otimização de custos**
  - Análise de uso das Lambdas e S3
  - Políticas de retenção de arquivos antigos

---

## 5. Segurança e LGPD
- [ ] **Criptografia de dados sensíveis**
- [ ] **Política de retenção e exclusão de dados**
- [ ] **Auditoria de acessos e ações**

---

## 6. Experiência do Desenvolvedor
- [ ] **Ambiente de desenvolvimento local fácil (Docker, scripts, mocks)**
- [ ] **Templates para issues, PRs e changelog**
- [ ] **Onboarding automatizado**

---

## 7. Roadmap Visual
- [ ] **Quadro Kanban (GitHub Projects, Jira, Trello)**
- [ ] **Releases e milestones bem definidos**

---

## Próximos Passos
1. Priorizar os itens mais importantes para o negócio.
2. Quebrar tarefas grandes em issues menores.
3. Definir responsáveis e prazos.
4. Revisar o plano a cada sprint/ciclo. 