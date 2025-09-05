-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    senha_hash TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Especialidades
CREATE TABLE IF NOT EXISTS especialidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questões
CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especialidade_id INTEGER NOT NULL,
    enunciado TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('objetiva','pratica')) NOT NULL DEFAULT 'objetiva',
    alternativas TEXT,  -- JSON como string
    resposta_correta TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (especialidade_id) REFERENCES especialidades(id) ON DELETE CASCADE
);

-- Provas
CREATE TABLE IF NOT EXISTS provas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nome TEXT
    especialidade_id INTEGER NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arquivo_pdf TEXT,
    arquivo_gabarito TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (especialidade_id) REFERENCES especialidades(id) ON DELETE CASCADE
);

-- Questões em cada prova
CREATE TABLE IF NOT EXISTS questoes_prova (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prova_id INTEGER NOT NULL,
    questao_id INTEGER NOT NULL,
    ordem INTEGER NOT NULL,
    FOREIGN KEY (prova_id) REFERENCES provas(id) ON DELETE CASCADE,
    FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE
);

-- Exemplo de gatilho: atualiza 'criado_em' da questão ao inserir
CREATE TRIGGER IF NOT EXISTS atualiza_criado_em_questao
AFTER INSERT ON questoes
FOR EACH ROW
BEGIN
    UPDATE questoes
    SET criado_em = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;