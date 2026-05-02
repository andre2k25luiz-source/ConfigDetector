# ConfigDetector
## 🚀 AutoML YOLO (One-Shot Object Detection)
arquiteturas inteligentes para detector configurável de objetos.

Sistema de **AutoML para Visão Computacional** capaz de treinar um modelo de detecção de objetos utilizando **apenas uma única imagem de entrada (one-shot)**.

O pipeline gera automaticamente um dataset sintético e treina um modelo baseado em **YOLOv8**.

---

## 🧠 Como funciona

O sistema segue o seguinte fluxo:

1. 📸 Usuário envia uma imagem com o objeto
2. ✂️ O objeto é recortado automaticamente
3. 🧩 O sistema gera imagens sintéticas (data synthesis)
4. 🏋️ O modelo YOLO é treinado automaticamente
5. 🔍 O modelo pode ser usado para detectar objetos em novas imagens

---

## 📁 Estrutura do Projeto

```
ConfigDetector/
│
├── app.py                         # Aplicação principal (Flask)
├── requirements.txt               # Dependências do projeto
├── README.md                      # Documentação
├── .gitignore                     # Arquivos ignorados pelo Git
│
├── routes/                        # Rotas da API
│   ├── __init__.py
│   ├── main_rote.py               # Rota principal
│   ├── predict_route.py           # Rota de predição
│   ├── train_route.py             # Rota de treinamento
│   └── save_yolo_route.py         # Rota para salvar no formato YOLO
│
├── services/                      # Regras de negócio
│   ├── __init__.py
│   ├── predict_service.py         # Lógica de inferência
│   └── train_service.py           # Lógica de treinamento
│
├── utils/                         # Funções auxiliares
│   ├── __init__.py
│   ├── generator_utils.py         # Geração de dataset sintético
│   └── criar_diretorios_utils.py  # Criação de diretórios
│
├── templates/                     # Frontend (HTML)
│   └── index.html
│
├── static/                        # Arquivos estáticos
│   ├── css/
│   │   └── index.css
│   ├── js/
│   │   └── index.js
│   └── images/
│       ├── ai-and-automation-icon-vector.ico
│       └── images.png
│
├── data/                          # Dados do projeto
│   ├── input/                     # Imagens de entrada
│   ├── backgrounds/               # Imagens de fundo
│   └── output/
│       ├── images/                # Imagens geradas
│       └── labels/                # Labels YOLO
```

---

## ⚙️ Instalação

Clone o projeto e instale as dependências:

```bash
git clone https://github.com/andre2k25luiz-source/AUTOML_YOLO.git
cd automl_yolo

pip install -r requirements.txt
```

---

## ▶️ Como Executar

### 🔹 Iniciar a API (Flask)

```bash
python3 app.py
```

A API estará disponível em:

```
http://localhost:5000
```

---

## 📌 Pré-requisitos IMPORTANTES

Antes de treinar, você precisa adicionar imagens de fundo:

```
data/backgrounds/
```

Exemplo:

```
backgrounds/
├── bg1.jpg
├── bg2.jpg
├── bg3.jpg
```

⚠️ Sem isso o sistema não funciona.

---

## 📡 Endpoints da API

### 🔹 Treinar modelo

```
POST /train
```

**Body:**

* `image` (file)

**Descrição:**

* Gera dataset sintético
* Treina modelo automaticamente
* Salva em: `models/best.pt`

---

### 🔹 Fazer predição

```
POST /predict
```

**Body:**

* `image` (file)

**Retorno:**

* Bounding boxes detectadas

---

## 🏋️ Treinamento

O modelo utilizado é o **YOLOv8 (Ultralytics)**.

O sistema automaticamente:

* gera dataset sintético
* cria `data.yaml`
* executa o treinamento

---

## ⚠️ Limitações

* Segmentação simples (threshold)
* Sem sombras realistas
* Sem oclusão de objetos
* Pode não generalizar bem com poucos backgrounds

---

## 🚀 Melhorias Futuras

* Segmentação avançada com SAM
* Geração de dados com Stable Diffusion
* Multi-classe automática
* Sistema de cache de modelos
* Deploy em nuvem

---

## 💡 Objetivo

Este projeto demonstra como transformar:

👉 **1 imagem → dataset sintético → modelo funcional**

Utilizando conceitos modernos de:

* Data-centric AI
* Synthetic Data
* AutoML

---

## 📜 Licença

Este projeto é open-source e pode ser utilizado para fins educacionais e comerciais.

---

## 👨‍💻 Autor

Desenvolvido por André Luiz
