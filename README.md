# PDF Page Cropper

The PDF Page Cropper splits every page in a PDF into multiple equal parts.

It supports left-to-right splitting and top-to-bottom splitting, which makes it useful for scanned spreads, multi-column layouts, or pages that need to be separated into equal segments while preserving vector PDF output through PyMuPDF.

## Features

- Split all pages in a PDF into equal parts
- Support horizontal splitting from left to right
- Support vertical splitting from top to bottom
- Output `parts` pages for each input page
- Preserve PDF content without rasterizing pages
- Handle rotated pages before splitting
- Support automatic output naming
- Prevent accidental overwrite unless `--overwrite` is provided

## Requirements

- Python 3
- PyMuPDF

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```bash
python main.py input.pdf
```

This will create:

```bash
input_split.pdf
```

By default, each page is split into 2 equal horizontal parts, which means left 50% and right 50%.

Specify an output path:

```bash
python main.py input.pdf -o output.pdf
```

Split each page into 3 equal parts from left to right:

```bash
python main.py input.pdf --parts 3 --direction horizontal
```

Split each page into 4 equal parts from top to bottom:

```bash
python main.py input.pdf --parts 4 --direction vertical
```

Overwrite an existing output file:

```bash
python main.py input.pdf -o output.pdf --overwrite
```

Combine all options:

```bash
python main.py input.pdf -o output.pdf --parts 4 --direction vertical --overwrite
```

Show version:

```bash
python main.py --version
```

## Parameters

- `input.pdf`: input PDF path
- `-o`, `--output`: output PDF path
- `--parts`: number of equal parts per page, minimum `2`, default `2`
- `--direction`: split direction, `horizontal` for left-to-right or `vertical` for top-to-bottom
- `--overwrite`: overwrite an existing output file
- `--version`: show the current date-based version

## Behavior

- Input pages are split into `parts` equal segments
- `horizontal` means left-to-right splitting
- `vertical` means top-to-bottom splitting
- Rotated pages are normalized in memory before splitting
- The input file is never modified
- If the input has `N` pages, the output will have `N * parts` pages

Successful output example:

```text
done: output.pdf (2 input pages -> 8 output pages)
```

## How to Build

Build Windows/Linux/macOS executable binary file via PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build a single executable:

```bash
pyinstaller --onefile --noupx -i icon.ico --name pdf-cropper main.py
```

After the build finishes, the executable will be generated in:

```bash
dist/
```
