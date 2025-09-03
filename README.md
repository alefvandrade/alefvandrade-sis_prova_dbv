# alefvandrade-sis_prova_dbv
Sistema python que faz provas pra especialidade de desbravadores

Documentação do Sistema de Provas - Vicuna AI
Estrutura de Pastas
Backend/
    Controllers/          # Controladores do sistema
    Database/             # Conexão e migrations do banco SQLite
        __init__.py
        connection.py
        migrations.sql
    Models/               # Classes principais (ORM-like)
        __init__.py
        usuario.py
        especialidade.py
        prova.py
        questao.py
        multipla.py
        dissertativa.py
        pratica.py
    Services/             # Serviços do sistema
        __init__.py
        ia_questions.py  # Serviço que conecta com a Vicuna API
        pdf_generator.py # Geração de PDF/Doc
        utils.py         # Funções auxiliares
Data/
    Input/                # PDFs de entrada
    Output/               # DOC/PDF de saída
    sis_prova_dbv.sqlite  # Banco de dados SQLite
Frontend/
    config.ini            # Configurações
    main.py               # Interface ou script principal
test_db.py               # Script para testes do DB
README.md

Fluxo do Sistema

Upload do PDF de Questões

Usuário coloca arquivos PDF na pasta Data/Input/.

Serviço pdf_generator.py faz a leitura e extração de textos.

Função principal: extrair_texto_pdf(pdf_path).

Leitura e Processamento do Conteúdo

O texto extraído do PDF é processado para identificar:

Enunciados

Tipos de questão (múltipla, dissertativa, prática)

Conteúdo / tema

Utiliza utilitários de utils.py para normalização de strings e limpeza de dados.

Banco de Dados

Banco: SQLite (sis_prova_dbv.sqlite)

Tabelas principais:

usuarios → cadastro de usuários

especialidades → áreas de conhecimento

provas → provas geradas

questoes → questões, relacionadas a provas

Conexão: Backend/Database/connection.py com classe DatabaseConnection encapsulando execução/consulta.

Modelos / Classes

Usuario, Especialidade → cadastro e CRUD básico.

Prova → gerenciamento da prova, armazenamento de questões.

Questao → superclasse para questões:

QuestaoMultipla

QuestaoDissertativa

QuestaoPratica

Cada classe possui métodos de CRUD (cadastrar, buscar_por_id, listar_todos, atualizar, excluir).

Integração com IA (Vicuna)

Arquivo: Backend/Services/ia_questions.py

Função principal: gerar_questao(tipo, tema, dificuldade="media")

Fluxo:

Recebe tipo de questão, tema e dificuldade

Monta prompt apropriado para Vicuna

Chama API via requests.post com header Authorization: Bearer SUA_CHAVE_API_VICUNA

Retorna enunciado, alternativas (quando múltipla) e gabarito

Cada classe de questão chama esse serviço para gerar conteúdo dinâmico.

Geração de Prova Final

Arquivo: pdf_generator.py

Funções principais:

gerar_doc_prova(prova_id) → gera DOC/PDF com todas as questões

incluir_gabarito() → adiciona gabarito separado no final do documento

Saída salva em Data/Output/.

Workflow Completo

Usuário envia PDF → pdf_generator.py extrai texto.

Serviço identifica tipos de questão → instancia classes Questao*.

Cada questão chama Vicuna para gerar conteúdo.

Questões são salvas no banco via métodos CRUD.

Classe Prova organiza questões e gera DOC/PDF com gabarito.

Arquivo final disponível em Data/Output/.

Exemplo de Uso
from Backend.Models.prova import Prova
from Backend.Services.pdf_generator import gerar_doc_prova

# Criar prova
nova_prova = Prova(codigo="PROVA01", nome="Simulado ENEM")
nova_prova.cadastrar()

# Gerar questões usando Vicuna
from Backend.Services.ia_questions import gerar_questao

q1_texto = gerar_quest