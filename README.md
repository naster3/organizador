# organizador de archivos

## version

1.0.3

Una CLI (lÃ­nea de comandos) para organizar carpetas tipo **Descargas** o **Escritorio**:
- por **tipo** (extensiÃ³n) â†’ `Images/`, `Documents/`, etc.
- por **fecha** â†’ `2026/02/`
- con **simulaciÃ³n** (`--dry-run`) y **deshacer** (`undo`) para no jugar ruleta rusa con tus archivos.

> Este repo antes era un script suelto. Ahora es un comando instalable. MÃ¡s Ãºtil, menos drama.

## InstalaciÃ³n (desarrollo)

```bash
git clone https://github.com/naster3/organizador.git
cd organizador

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

## Uso rÃ¡pido

### 1) Simular (no mueve nada)
```bash
organizador run "C:\Users\TU_USER\Downloads" --mode type --dry-run
```

### 2) Ejecutar de verdad
```bash
organizador run "C:\Users\TU_USER\Downloads" --mode type
```

### 3) Organizar por fecha (aÃ±o/mes)
```bash
organizador run "C:\Users\TU_USER\Downloads" --mode date --group-by month
```

### 4) Deshacer la Ãºltima corrida
```bash
organizador undo "C:\Users\TU_USER\Downloads"
```

## Reglas

Por defecto el proyecto trae reglas sensatas por extensiÃ³n (imÃ¡genes, docs, video, audio, etc.).
TambiÃ©n puedes pasar un JSON de reglas personalizadas:

```bash
organizador run ~/Downloads --mode type --rules rules.json
```

`rules.json` ejemplo:

```json
{
  "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
  "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
  "Code": [".py", ".js", ".ts", ".html", ".css"],
  "Archives": [".zip", ".rar", ".7z"]
}
```

## Seguridad (para dormir tranquilo)

- `--dry-run` para ver cambios antes
- genera un **journal** (log) por corrida en: `TU_CARPETA/.organizador/journals/`
- `undo` revierte usando ese journal

## Desarrollo

```bash
pip install -e .[dev]  # (si luego agregas extras dev)
pytest
ruff check .
```

## Licencia
MIT
