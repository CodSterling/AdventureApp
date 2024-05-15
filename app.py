from flask import Flask, request, render_template_string, Markup, url_for

app = Flask(__name__)


class Paths:

    @classmethod
    def path1(cls, direction):
        options = {
            "right": "pass",
            "left": "blocked",
            "up": "trapped",
            "down": "door"
        }
        return options.get(direction, "Invalid direction")

    @classmethod
    def path2(cls, direction):
        options = {
            "right": "blocked",
            "left": "trapped",
            "up": "pass",
            "down": "door"
        }
        return options.get(direction, "Invalid direction")

    @classmethod
    def path3(cls, direction):
        options = {
            "right": "door",
            "left": "pass",
            "up": "blocked",
            "down": "trapped"
        }
        return options.get(direction, "Invalid direction")

    @classmethod
    def path4(cls, direction):
        options = {
            "right": "trapped",
            "left": "door",
            "up": "pass",
            "down": "blocked"
        }
        return options.get(direction, "Invalid direction")

    @classmethod
    def path5(cls, direction):
        options = {
            "right": "pass",
            "left": 'DOOR! Here is a prize! '
                    '<a href="https://opensea.io/assets/matic/0x43668e306dba9172824524fd2c0c6924e710ea5b/191" '
                    'target="_blank">OpenSea Link</a>',
            "up": "trapped",
            "down": "blocked"
        }
        return options.get(direction, "Invalid direction")


paths = Paths()


@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Choose Your Path</title>
            <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
        </head>
        <body>
            <h1>Choose Your Path</h1>
            <form action="/choose" method="post">
                <label for="path">Choose a path (1-5):</label>
                <input type="number" id="path" name="path" min="1" max="5" required>
                <br><br>
                <label for="direction">Choose a direction (right, left, up, down):</label>
                <input type="text" id="direction" name="direction" required>
                <br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    ''')


@app.route('/choose', methods=['POST'])
def choose():
    path_num = int(request.form['path'])
    direction = request.form['direction'].lower()

    path_method = getattr(paths, f'path{path_num}', None)
    if path_method:
        result = path_method(direction)
        # Mark the result as safe HTML
        result = Markup(result)
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Result</title>
                <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
            </head>
            <body>
                <h1>Result</h1>
                <p>Path {{ path_num }} going {{ direction }}: {{ result }}</p>
                <a href="/">Go back</a>
            </body>
            </html>
        ''', path_num=path_num, direction=direction, result=result)
    else:
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error</title>
                <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
            </head>
            <body>
                <h1>Error</h1>
                <p>Invalid path number.</p>
                <a href="/">Go back</a>
            </body>
            </html>
        ''')


if __name__ == '__main__':
    app.run(debug=True)
