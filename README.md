# Crypto Data Pipeline

Pipeline de engenharia de dados que coleta informações de criptomoedas da API pública CoinGecko, processa e armazena em um Data Lake na AWS S3 seguindo a arquitetura medalhão (Bronze, Prata e Ouro), orquestrado pelo Apache Airflow containerizado com Docker.

## Sobre o projeto

Este projeto foi construído com o objetivo de praticar e demonstrar o fluxo completo de um pipeline de dados, desde a ingestão de dados brutos até a entrega de métricas prontas para consumo. A ideia é simples: consumir uma API pública diariamente, transformar os dados em etapas bem definidas e armazenar tudo de forma organizada na nuvem.

A API escolhida foi a CoinGecko, que fornece dados gratuitos sobre as maiores criptomoedas do mercado, incluindo preço, capitalização, volume de negociação e recordes históricos.

## Arquitetura

O pipeline segue a arquitetura medalhão com três camadas:

**Bronze:** recebe os dados brutos da API exatamente como vieram, em formato JSON. Nenhuma transformação é aplicada. Essa camada funciona como backup da verdade e permite reprocessamento futuro.

**Prata:** lê os dados do Bronze, aplica limpeza e padronização. Colunas desnecessárias são removidas, tipos de dados são corrigidos (datas, números), valores nulos são tratados e o formato é convertido para Parquet. Os dados ficam prontos para análise.

**Ouro:** lê os dados da Prata e gera métricas de negócio. Calcula a dominância de mercado de cada moeda, a volatilidade nas últimas 24 horas, o volume relativo ao market cap e organiza um ranking. Essa camada entrega uma tabela final enxuta e focada, pronta para dashboards ou consultas diretas.

O fluxo completo:

```
CoinGecko API → extract.py → S3 Bronze (JSON)
                                  ↓
                transform.py → S3 Prata (Parquet)
                                  ↓
                aggregate.py → S3 Ouro (Parquet)
```

O Apache Airflow orquestra todas as etapas, executando o pipeline diariamente de forma automática. Se uma etapa falhar, o Airflow tenta novamente até duas vezes antes de marcar como falha.

## Tecnologias

| Tecnologia | Uso no projeto |
|---|---|
| Python | Linguagem principal para extração, transformação e carga |
| Apache Airflow 2.10.5 | Orquestração e agendamento do pipeline |
| Docker e Docker Compose | Containerização do Airflow e PostgreSQL |
| AWS S3 | Data Lake com arquitetura medalhão |
| boto3 | Biblioteca Python para integração com a AWS |
| pandas | Manipulação e transformação de dados |
| Parquet (PyArrow) | Formato colunar para armazenamento eficiente |
| Git | Versionamento de código com commits semânticos |

## Estrutura do projeto

```
crypto-pipeline/
│
├── dags/
│   └── crypto_pipeline_dag.py        # DAG do Airflow que orquestra o pipeline
│
├── src/
│   ├── extract/
│   │   ├── __init__.py
│   │   └── extract.py                # Consome a API CoinGecko
│   │
│   ├── transform/
│   │   ├── __init__.py
│   │   └── transform.py              # Limpeza e padronização dos dados
│   │
│   ├── aggregate/
│   │   ├── __init__.py
│   │   └── aggregate.py              # Cálculo de métricas de negócio
│   │
│   └── load/
│       ├── __init__.py
│       └── load.py                   # Funções de salvamento no S3
│
├── data/                              # Exemplos de dados (amostra local)
│   ├── raw/
│   │   └── 2026-05-09/
│   │       └── crypto_raw.json
│   ├── transformed/
│   │   └── 2026-05-09/
│   │       └── crypto_transformed.parquet
│   └── aggregated/
│       └── 2026-05-09/
│           └── crypto_aggregated.parquet
│
├── docker-compose.yaml               # Configuração do Airflow containerizado
├── requirements.txt                   # Dependências Python do projeto
├── .env                               # Variáveis de ambiente (não versionado)
└── .gitignore
```

A pasta `data/` contém apenas uma amostra dos dados para fins de visualização. Os dados reais do pipeline são armazenados no AWS S3, organizados por data em cada camada (bronze, prata e ouro).

## Como rodar o projeto

### Pré-requisitos

Você vai precisar ter instalado na sua máquina: Docker e Docker Compose, Python 3.10 ou superior, AWS CLI configurado com credenciais válidas e uma conta AWS com um bucket S3 criado.

### Configuração

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/crypto-data-pipeline.git
cd crypto-data-pipeline
```

2. Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
BUCKET_NAME=nome-do-seu-bucket
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_DEFAULT_REGION=us-east-1
```

3. Suba o Airflow:

```bash
docker-compose up -d
```

4. Acesse a interface do Airflow em `localhost:8080` com usuário `admin` e senha `admin`.

5. Ative a DAG `crypto_pipeline` e dispare uma execução manual ou aguarde o agendamento diário.

### Verificando os dados

Para confirmar que o pipeline funcionou, consulte os arquivos no S3:

```bash
aws s3 ls s3://nome-do-seu-bucket/ --recursive
```

Você verá os arquivos organizados por data em cada camada (bronze, prata, ouro).

## Métricas calculadas na camada Ouro

| Métrica | Descrição |
|---|---|
| dominancia_mercado | Percentual que cada moeda representa do market cap total |
| volatilidade_24h | Diferença entre o preço máximo e mínimo nas últimas 24 horas |
| volume_por_market_cap | Volume negociado em relação ao tamanho da moeda (em percentual) |
| ranking | Posição da moeda ordenada por capitalização de mercado |