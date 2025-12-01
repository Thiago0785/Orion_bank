import sys
from pathlib import Path
# Ensure repository root is on sys.path so Python finds the package
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
from orion_flask_project.app import app
from flask import render_template


def render_and_check(template_name):
    with app.test_request_context('/'):
        html = render_template(template_name)
        print(f"Rendered {template_name}: length={len(html)}")
        exists_btn = 'id="gemini-support-btn"' in html
        exists_modal = 'id="gemini-modal"' in html
        print(f"  gemini-support-btn present: {exists_btn}")
        print(f"  gemini-modal present: {exists_modal}")
        assert exists_btn and exists_modal, f"Modal or button not found in {template_name}"


if __name__ == '__main__':
    for t in ['index.html', 'dashboard.html', 'admin_dashboard.html', 'desenvolvimento.html']:
        render_and_check(t)
    print('All tested templates contain Gemini modal and button.')
