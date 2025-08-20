document$.subscribe(() => {
if (typeof renderMathInElement !== 'undefined') {
renderMathInElement(document.body, {
delimiters: [
{ left: "$$", right: "$$", display: true },
{ left: "\\(", right: "\\)", display: false }
]
});
}
});
