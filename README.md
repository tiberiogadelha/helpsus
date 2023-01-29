# HELPSUS!

HelpSUS! é um projeto desenvolvido por Tibério Mahon como tema de TCC para o curso de Ciência da Computação, na Universidade Federal de Campina Grande (UFCG) campus I.


O sistema usando Django no padrão MVT foi desenvolvido após observar um grande problema que acometia as Unidades de Pronto Atendimento (UPA) da cidade de Campina Grande: trabalho dos profissionais era extremamente manual e repetitivo, usando fichas de papel.

Sendo assim, o sistema surge para resolver estes problemas, sendo um prontuário eletrônico baseado na metodologia usada em UPAs.


### 📋 Pré-requisitos

Para rodar o sistema é necessário ter instalado Python na versão >= 3.6 e uma instância de PostgreSQL

### 🔧 Instalação

Após instalar os pré-requisitos, é necessário configurar o arquivo settings.py. Necessário informar as credenciais do banco de dados.


Para instalar as dependências é recomendado que use um VirtualEnv do Python. As depedências são instaladas com o seguinte comando: 
```shell
pip3 install -r requirements.txt
```

Feito isso, será necessário configurar o banco de dados com as tabelas necessárias para o HelpSUS!. Essa configuração deve ser feita com os seguintes comandos (de forma sequencial):

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

E por fim, para rodar o servidor na máquina:
```shell
python3 manage.py runserver
```

Com o servidor rodando, o sistema pode ser acesso pela porta padrão :8080
