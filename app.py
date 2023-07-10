
from flask import Flask, request
import undetected_chromedriver as uc
import time
import traceback

clf_sig = "<title>Just a moment...</title>"

app = Flask(__name__)
driver = uc.Chrome(headless=True)

@app.route('/')
def index():
    return 'INDEX'


@app.route('/bypass')
def bypass():
    try:
        url = request.args.get('url', default='')
        time_out = int(request.args.get('time_out', default='15'))

        driver.get(url)

        time1 = time.time()

        html_content = ''
        was_timed_out = False

        while True:
            if (time.time() - time1) > time_out:
                was_timed_out = True
                break

            html_content = driver.page_source

            if clf_sig not in html_content:
                break
            else:
                time.sleep(1)
                continue
        
        driver.close()
        if was_timed_out:
            return {'error': 'timed_out'}, 200
        else:
            return {'html_content': html_content}
    except Exception as ex:
        return {'error': str(ex), 'trace_back': traceback.format_exc()}


if __name__ == '__main__':
    app.run()
