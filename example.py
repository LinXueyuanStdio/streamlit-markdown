import streamlit as st

from st_diff_viewer import diff_viewer

old_text = """\
const a = 10
const b = 10
const c = () => console.log('foo')

if(a > 10) {
  console.log('bar')
}

console.log('done')\
"""

new_text = """\
const a = 10
const boo = 10

if(a === 10) {
  console.log('bar')
}\
"""

old_col, new_col = st.columns(2)
old_text = old_col.text_area("Old Text", old_text, height=250)
new_text = new_col.text_area("New Text", new_text, height=250)

left_col, right_col = st.columns(2)
left_title = left_col.text_input("Left Title", "old")
right_title = right_col.text_input("Right Title", "new")

check1, check2, check3 = st.columns(3)
split_view = check1.checkbox("Split View", True)
use_dark_theme = check2.checkbox("Use Dark Theme", False)
hide_line_numbers = check3.checkbox("Hide Line Numbers", False)

col1, col2 = st.columns(2)
extra_lines_surrounding_diff = col1.number_input("Extra Lines Surrounding Diff", 3)
highlight_lines = col2.text_area("Highlight Lines", "").split("\n")

diff_viewer(
    old_text,
    new_text,
    split_view=split_view,
    use_dark_theme=use_dark_theme,
    left_title=left_title,
    right_title=right_title,
    extra_lines_surrounding_diff=extra_lines_surrounding_diff,
    hide_line_numbers=hide_line_numbers,
    highlight_lines=highlight_lines,
)
