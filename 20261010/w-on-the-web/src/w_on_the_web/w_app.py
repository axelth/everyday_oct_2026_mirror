import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


class WRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        w_run = subprocess.run('w', capture_output=True)
        result = w_run.stdout
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.make_html(result))

    def make_html(self, result: bytes) -> bytes:
        res_str = result.decode("utf8")
        return (
            f"""<html>
            <head><title>w output</title></head>
            <style>
            pre {{
              background-color: black;
              color: white;
              padding: 5px;
            }}
            </style>
               <body>
                  <pre>
            
            {res_str}
            
                    </pre>
                </body>
            </html>
            
            """.encode("utf8")
        )


def run(server_class=HTTPServer, handler_class=WRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

