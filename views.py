import os
from flask import Flask, request, redirect, render_template

import dars_parser, minor_parser, progress_checker

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = ['pdf']

def file_allowed(filename):
    file_extension = filename.rsplit('.', 1)[1].lower()
    extension_allowed = file_extension in app.config["ALLOWED_EXTENSIONS"]
    return '.' in filename and extension_allowed

@app.before_first_request
def load_minor_data():
    df = minor_parser.create_pd('minor_data.csv')
    minors = minor_parser.create_minors(df)

    pass


@app.route('/', methods=['GET', 'POST'])
def upload_image():

    if request.method == 'POST':

        if request.files:

            pdf = request.files['file']

            if pdf.filename == '':
                # print('file must have nonempty filename') # show this on webpage
                return redirect(request.url)

            if not file_allowed(pdf.filename):
                # print('extension not allowed') # show this on webpage
                return redirect(request.url)

            # pass info from here into html for visuals
            pdf_text = dars_parser.convert_pdf_to_text(pdf) # .pdf to one long string
            course_text = dars_parser.get_courses_from_text(pdf_text) # extract course list from string
            courses = dars_parser.put_courses_into_tuples(course_text) # put course text into list of tuples
            # for c in courses:
            #     print(c)
            df = minor_parser.create_pd('minor_data.csv')
            minors = minor_parser.create_minors(df)
            csminor = minors[10]
            info = []
            for g in csminor.required_groups:
                info.append(progress_checker.check_C_type_group(g, courses))

            return render_template('index.html', courses = courses, info = info)

    return render_template('index.html')


# this allows running "python3 views.py" to start server
if __name__ == '__main__':
    app.run(debug=True)
