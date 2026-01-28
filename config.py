from pathlib import Path

# Определяем пути загрузки исходников и сохранения результата
path_sources = Path(__file__).parent / "sources"
path_results = Path(__file__).parent / "results"

# Цвета для вывода
colors = {"green": '\033[92m', "end": '\033[0m'}
