import argparse
from pathlib import Path
import sys

import fitz  # PyMuPDF


def parse_args():
    parser = argparse.ArgumentParser(
        description="Split each PDF page into left and right 50% pages."
    )
    parser.add_argument(
        "input_pdf",
        nargs="?",
        default="input.pdf",
        help="Path to the input PDF file. Defaults to input.pdf.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output PDF file. Defaults to <input>_split.pdf.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output PDF if it already exists.",
    )
    return parser.parse_args()


def default_output_path(input_pdf):
    input_path = Path(input_pdf)
    return str(input_path.with_name(f"{input_path.stem}_split.pdf"))


def split_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    out = fitz.open()
    input_page_count = doc.page_count

    for page_index, page in enumerate(doc):
        if page.rotation:
            page.set_rotation(0)

        rect = page.rect
        mid_x = rect.width / 2

        # left half page
        left_rect = fitz.Rect(0, 0, mid_x, rect.height)
        left_page = out.new_page(width=mid_x, height=rect.height)
        left_page.show_pdf_page(left_page.rect, doc, page_index, clip=left_rect)

        # right half page
        right_rect = fitz.Rect(mid_x, 0, rect.width, rect.height)
        right_page = out.new_page(width=mid_x, height=rect.height)
        right_page.show_pdf_page(right_page.rect, doc, page_index, clip=right_rect)

    out.save(output_pdf)
    return input_page_count, out.page_count


if __name__ == "__main__":
    args = parse_args()
    input_path = Path(args.input_pdf)

    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_pdf = args.output or default_output_path(args.input_pdf)
    output_path = Path(output_pdf)

    if output_path.resolve() == input_path.resolve():
        print(
            "error: output file must be different from input file",
            file=sys.stderr,
        )
        sys.exit(1)

    if output_path.exists() and not args.overwrite:
        print(
            f"error: output file already exists: {output_path} (use --overwrite to replace it)",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        input_page_count, output_page_count = split_pdf(args.input_pdf, output_pdf)
    except fitz.FileDataError:
        print(
            f"error: invalid PDF file or corrupted content: {input_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"done: {output_pdf} ({input_page_count} input pages -> {output_page_count} output pages)"
    )
