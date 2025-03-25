from flask import Flask, render_template


def create(app_name='graphdb_boss_ui', javascript_plugin_files=None):
    app = Flask(app_name, template_folder='graphdb_boss/ui/templates', static_folder='graphdb_boss/ui/static')

    @app.route('/')
    def get_index():
        return render_template('index.html', javascript_plugin_files=javascript_plugin_files)

    @app.context_processor
    def utility_processor():

        def get_file_contents(filepath):
            with open(filepath) as f:
                return f.read()

        return dict(get_plugin_files=get_file_contents)

    return app
