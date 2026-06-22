# latexmk configuration for Politecnico di Torino thesis
$pdf_mode = 1;              # Use pdflatex
$pdflatex = "pdflatex --shell-escape -interaction=nonstopmode %O %S";
$biber = "biber %O %S";
$aux_dir = "build";         # Auxiliary files go here; PDF stays in root
$max_repeat = 3;            # Max number of pdflatex runs
