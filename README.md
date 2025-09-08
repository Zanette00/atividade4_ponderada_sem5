# Page View Time Series Visualizer

Projeto acadêmico (freeCodeCamp) para visualizar séries temporais de visualizações de páginas usando Pandas, Matplotlib e Seaborn.

## Como executar

1. Crie e ative um ambiente virtual (opcional, mas recomendado).
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Baixe o dataset `fcc-forum-pageviews.csv` (este repositório já inclui um script de download no `main.py` caso necessário) ou coloque-o na raiz do projeto.
4. Execute:
   ```bash
   python main.py
   ```

As imagens geradas serão salvas como `line_plot.png`, `bar_plot.png` e `box_plot.png` na raiz do projeto.

## Testes

Execute os testes com:
```bash
python -m pytest -q | cat
```

## Estrutura

- `time_series_visualizer.py`: funções principais (`draw_line_plot`, `draw_bar_plot`, `draw_box_plot`).
- `main.py`: ponto de entrada para gerar os gráficos e (opcionalmente) baixar o dataset.
- `test_module.py`: testes automatizados.
- `requirements.txt`: dependências Python.


