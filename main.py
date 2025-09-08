import sys
from pathlib import Path

import time_series_visualizer as tsv

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    dataset_path = project_root / "fcc-forum-pageviews.csv"

    if not dataset_path.exists():
        try:
            # Força carregamento que também tenta baixar no módulo
            _ = tsv.df
        except Exception as e:  # noqa: BLE001
            print(e)
            sys.exit(1)

    print("Gerando gráficos...")
    tsv.draw_line_plot()
    tsv.draw_bar_plot()
    tsv.draw_box_plot()
    print("Gráficos salvos: line_plot.png, bar_plot.png, box_plot.png")
