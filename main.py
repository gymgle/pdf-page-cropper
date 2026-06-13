import argparse
from pathlib import Path
import sys
import fitz  # PyMuPDF


VERSION = "v2026.06.13"


def positive_parts(value):
    parts = int(value)
    if parts < 2:
        raise argparse.ArgumentTypeError(
            "parts must be an integer greater than or equal to 2"
        )
    return parts


def parse_args():
    parser = argparse.ArgumentParser(
        description="Split each PDF page into equal parts horizontally or vertically."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
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
    parser.add_argument(
        "--parts",
        type=positive_parts,
        default=2,
        help="Number of equal parts per page. Defaults to 2.",
    )
    parser.add_argument(
        "--direction",
        choices=("horizontal", "vertical"),
        default="horizontal",
        help="Split direction: horizontal for left-to-right, vertical for top-to-bottom.",
    )
    return parser.parse_args()


def default_output_path(input_pdf):
    input_path = Path(input_pdf)
    return str(input_path.with_name(f"{input_path.stem}_split.pdf"))


def build_clips(rect, parts, direction):
    clips = []

    if direction == "horizontal":
        part_width = rect.width / parts
        for index in range(parts):
            left = part_width * index
            right = rect.width if index == parts - 1 else part_width * (index + 1)
            clip = fitz.Rect(left, 0, right, rect.height)
            clips.append((clip, clip.width, rect.height))
        return clips

    part_height = rect.height / parts
    for index in range(parts):
        top = part_height * index
        bottom = rect.height if index == parts - 1 else part_height * (index + 1)
        clip = fitz.Rect(0, top, rect.width, bottom)
        clips.append((clip, rect.width, clip.height))
    return clips


def split_pdf(input_pdf, output_pdf, parts, direction):
    doc = fitz.open(input_pdf)
    out = fitz.open()
    input_page_count = doc.page_count

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        if page.rotation:
            page.set_rotation(0)

        rect = page.rect
        for clip_rect, page_width, page_height in build_clips(rect, parts, direction):
            target_page = out.new_page(width=page_width, height=page_height)
            target_page.show_pdf_page(target_page.rect, doc, page_index, clip=clip_rect)

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
        input_page_count, output_page_count = split_pdf(
            args.input_pdf,
            output_pdf,
            args.parts,
            args.direction,
        )
    except fitz.FileDataError:
        print(
            f"error: invalid PDF file or corrupted content: {input_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"done: {output_pdf} ({input_page_count} input pages -> {output_page_count} output pages)"
    )
