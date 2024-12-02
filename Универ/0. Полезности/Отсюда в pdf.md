Никак. А так:
1.  Enhancing export
2. Там экспорт в .md
3. В этом md не работают:
	1. Excalidraw
	2. отображение других .md
	3. таблицы косячные - рекомендую все вектора в таблицах делать сразу через mathjax
	4. пап
4. #бля добавить бы сюда преамбулу
```bash
pandoc --pdf-engine=xelatex -V mainfont="Times New Roman" -V geometry:a4paper -V documentclass=article -p -H ../before_body.tex -o output.pdf "input.md"
```
