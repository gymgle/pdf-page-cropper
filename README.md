# PDF Page Cropper

The PDF Page Cropper splits every page in a PDF into two separate pages: the left 50% and the right 50%.

It is designed for cases where a scanned spread or two-column layout needs to be separated into single pages while preserving vector PDF output through PyMuPDF.

## Features

- Split all pages in a PDF into left and right halves
- Output 2 pages for each input page
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

Specify an output path:

```bash
python main.py input.pdf -o output.pdf
```

Overwrite an existing output file:

```bash
python main.py input.pdf -o output.pdf --overwrite
```

## Behavior

- Input pages are split into left 50% and right 50%
- Rotated pages are normalized in memory before splitting
- The input file is never modified
- If the input has `N` pages, the output will have `2N` pages

Successful output example:

```text
done: output.pdf (2 input pages -> 4 output pages)
```

## Error Handling

The script reports clear errors for these cases:

- Input file does not exist
- Input file is not a valid PDF or is corrupted
- Output path is the same as the input path
- Output file already exists and `--overwrite` was not provided

## Files

- [main.py](main.py): command-line script that performs the PDF split
- [requirements.txt](requirements.txt): project dependency list
